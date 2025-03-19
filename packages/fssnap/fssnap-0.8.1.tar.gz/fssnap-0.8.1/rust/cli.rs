#![allow(non_camel_case_types)]

use std::cmp::Ordering;
use std::env;
use std::collections::{HashMap};

use std::os::unix::fs::MetadataExt;
use std::fs;
use std::path::PathBuf;

use anyhow::{anyhow, Result};
use clap::{Parser, Subcommand};
use fst::{MapBuilder, Streamer};
use nix::sys::statfs;
use nix::sys::statfs::{statfs, FsType};
use walkdir::{DirEntry, WalkDir};

mod db;
mod utils;

use db::{Db, Meta, Mappings, db_read, db_write, unmap_uxpermvalue};
use utils::{uid_to_name, gid_to_name};


fn lexicographic_sorter(a: &DirEntry, b: &DirEntry) -> Ordering {

	/*
     * The only way to sort a filesystem tree lexicographically is to force
     * directory entries to be postfixed with std::path::MAIN_SEPARATOR_STR.
     * That way if we do the comparisons on the paths we will yield the
     * entries in the right order. PathBuf would strip these separators for
     * directories hence why we need to convert to OsString first.
     */

	let mut a_path = a.path().to_path_buf().into_os_string();
	let mut b_path = b.path().to_path_buf().into_os_string();

	if a.file_type().is_dir() {
		a_path.push(std::path::MAIN_SEPARATOR_STR);
	}
	if b.file_type().is_dir() {
		b_path.push(std::path::MAIN_SEPARATOR_STR);
	}

	return a_path.cmp(&b_path);
}


const NETWORKED_FILESYSTEMS: [FsType; 3]  = [
    statfs::NFS_SUPER_MAGIC,
    statfs::SMB_SUPER_MAGIC,
    statfs::FsType{0:0x1021997} /* define WSL drvfs magic fstype ourselves */
];

fn is_networked_fs(fstype: FsType) -> bool {
    return NETWORKED_FILESYSTEMS.contains(&fstype);
}

fn is_procfs(fstype: FsType) -> bool {
    statfs::PROC_SUPER_MAGIC == fstype
}

fn create_index(dbfilename: &String, indexes: &mut Vec<String>) -> Result<()> {

    /* sanity check the input */
    assert!(dbfilename.len() > 0);
    for idxdir in indexes.iter() {
        /* Check for a postfix `/` character as this causes issues with walkdir and the
         * lexicographic sorting. This seems an easier approach than stripping them ourselves. */
        if idxdir.len() > 1 && idxdir.chars().last().unwrap() == '/' {
            return Err(anyhow!("{} cannot end with /", idxdir));
        }
        let md = std::fs::metadata(idxdir)?;
        if !md.is_dir() {
            return Err(anyhow!("{} is not a directory", idxdir));
        }
        let st = statfs(idxdir.as_str())?;
        if is_networked_fs(st.filesystem_type()) {
            return Err(anyhow!("{} points to a networked filesystem", idxdir));
        }
        if is_procfs(st.filesystem_type()) {
            return Err(anyhow!("{} points to a proc filesystem", idxdir));
        }
    }

    /* Sort after the sanity checks so errors are returned in order the end-user expects */
    indexes.sort();

    let mut pathfst_builder = MapBuilder::memory();
    let mut pathcount: u64 = 0;

    let mut mappings = Mappings {
        uidmap: HashMap::new(),
        gidmap: HashMap::new(),
        uidnamemap: HashMap::new(),
        gidnamemap: HashMap::new()
    };

    let mut meta = Meta {
        pathcount: 0,
        dirnames: Vec::new(),
        annotated: Some(false)
    };

    let mut fstype_cache: HashMap<u64, FsType> = HashMap::new();

    for idxdir in indexes.iter() {

        let canondirname = fs::canonicalize(PathBuf::from(idxdir))?.into_os_string().into_string().unwrap();
        if meta.dirnames.contains(&canondirname) {
            panic!("refusing to index {} twice", canondirname);
        }
        meta.dirnames.push(canondirname.clone());

        /*
         * Most file tree walkers descend into subdirectories first before
         * processing any files. This is generally fine but as we want to use
         * a FST for storing the full file paths we cannot do this. The FST
         * wants data to be inserted in lexicographic order. To get walkdir to
         * iterate over the tree this way we use sort_by. This will result in
         * a tree being walked like the following sample:
         *
         *  intro.txt
         *  world/
         *  world-explanation.txt
         *  world/hello.txt
         *  world0.txt
         *  world1/bla.txt
         */
        let walker = WalkDir::new(canondirname)
            .follow_links(false)
            .contents_first(false)
            .sort_by(|a,b| lexicographic_sorter(a, b)
			);
        let mut it = walker.into_iter();
        loop {
            
            let entry = match it.next() {
                None => break,
                Some(Err(e)) => {
                    log::error!("{}", e);
                    continue;
                },
                Some(Ok(entry)) => entry,
            };

            let mut pathname = entry.path().to_path_buf().into_os_string().into_string().unwrap();
            log::trace!("{}", pathname);

            let ft = entry.file_type();

            let meta = entry.metadata()?;
            let mode = meta.mode();
            let uid = meta.uid();
            let gid = meta.gid();
            let dev = meta.dev();

            let mut ignore_dir = false;

            if ft.is_dir() {
                let pbuf = entry.path().to_path_buf();
                let mut dirname = pbuf.clone().into_os_string().into_string().unwrap();

                match fstype_cache.get(&dev) {
                    Some(_) => {},
                    None => {
                        log::debug!("Walking new filesystem via {dirname}");
                        let st = statfs(&pbuf)?;
                        let fstype = st.filesystem_type();
                        fstype_cache.insert(dev, fstype);
                        if is_networked_fs(fstype) {
                            log::warn!("Ignoring {dirname} as it points to a networked filesystem");
                            ignore_dir = true;
                        }                        
                        if is_procfs(fstype) {
                            log::warn!("Ignoring {dirname} as it points to a proc filesystem");
                            ignore_dir = true;
                        }
                    }
                }

                if !(dirname.len() == 1 && dirname.starts_with('/')) {
                    dirname.push_str(std::path::MAIN_SEPARATOR_STR);
                }
                pathname = dirname;
            }

            match mappings.uidnamemap.get(&uid) {
                Some(_) => {}
                None => {
                    let name = match uid_to_name(uid) {
                        Ok(n) => n,
                        Err(_) => uid.to_string()
                    };
                    log::debug!("Resolving uid {} to {}", uid, name);
                    mappings.uidnamemap.insert(uid.into(), name.to_string());
                }
            };

            match mappings.gidnamemap.get(&gid) {
                Some(_) => {}
                None => {
                    let (name, v) = match gid_to_name(gid) {
                        Ok(n) => (n.0, n.1),
                        Err(_) => (gid.to_string(), Vec::new())
                    };
                    log::debug!("Resolving gid {} to {} with group list {:?}", gid, name, v);
                    /* the first entry of the list of users part of the group is simply the group
                     * name so rewrite the vector accordingly and insert it in the map */
                    let mut newv = v.clone();
                    newv.insert(0, name);
                    mappings.gidnamemap.insert(gid.into(), newv);
                }
            };

            let mut tmp: u16;
            let uid = match mappings.uidmap.get(&uid) {
                Some(n) => *n,
                None => {
                    tmp = mappings.uidmap.len().try_into().unwrap();
                    log::debug!("Mapping uid {} to {}", gid, tmp);
                    mappings.uidmap.insert(uid, tmp);
                    tmp
                }
            };

            let gid = match mappings.gidmap.get(&gid) {
                Some(n) => *n,
                None => {
                    tmp = mappings.gidmap.len().try_into().unwrap();
                    log::debug!("Mapping gid {} to {}", gid, tmp);
                    mappings.gidmap.insert(gid, tmp);
                    tmp
                }
            };

            let mut value = db::map_uxpermvalue(mode, uid, gid);

            if ignore_dir {
                /* top bit causes it to be flagged as ignored path: this is really dirty
                 * as we now squat on the top bit of the encoded `gid` but we have room
                 * for 32767 gids and i sincerely doubt we will encounter ever a system
                 * where we have that many configured groups so in practice this should
                 * not be an issue whatsoever. */
                value |= 1 << 63;
                it.skip_current_dir();
            }

            pathfst_builder.insert(pathname, value)?;
            pathcount = pathcount + 1;

        }
    }

    meta.pathcount = pathcount;
    let ret = Db {
        mappings: mappings,
        fst: pathfst_builder.into_map(),
        meta: meta
    };

    db_write(&PathBuf::from(dbfilename), &ret)?;

    Ok(())
}

fn compare(old: &Db, new: &Db) -> Result<()> {
    let mut difference = new.fst.op().add(&old.fst).difference();
    while let Some((k, _vs)) = difference.next() {
        println!("+ added {}", String::from_utf8_lossy(k));
    }

    let mut difference = old.fst.op().add(&new.fst).difference();
    while let Some((k, _vs)) = difference.next() {
        println!("- deleted {}", String::from_utf8_lossy(k));
    }

    let mut same = old.fst.op().add(&new.fst).intersection();
    while let Some((k, vals)) = same.next() {
        let filename = String::from_utf8_lossy(k);

        /* order of the values is not guaranteed so check the index
         * value and based on that determine what is the old and what
         * is the new value */
        let mut oldv;
        let mut newv;
        if vals[0].index == 1 {
            oldv = vals[1].value;
            newv = vals[0].value;
        }
        else {
            newv = vals[1].value;
            oldv = vals[0].value;
        }

        let (oldmode, oldmappeduid, oldmappedgid) = unmap_uxpermvalue(oldv);
        let (newmode, newmappeduid, newmappedgid) = unmap_uxpermvalue(newv);

        if oldmode != newmode {
            println!(". mode changed {filename} from {oldmode:o} to {newmode:o}");
        }

        log::trace!("{}", String::from_utf8_lossy(k));

        let olduid = old.mappings.uid_mapback_incl_username(oldmappeduid);
        let newuid = new.mappings.uid_mapback_incl_username(newmappeduid);
        if olduid.0 != newuid.0 {
            println!(". uid changed {filename} from {} ({}) to {} ({})",
                olduid.0, olduid.1, newuid.0, newuid.1);
        }

        let oldgid = old.mappings.gid_mapback_incl_username(oldmappedgid);
        let newgid = new.mappings.gid_mapback_incl_username(newmappedgid);
        if oldgid.0 != newgid.0 {
            println!(". gid changed {filename} from {} ({}) to {} ({})",
                oldgid.0, oldgid.1, newgid.0, newgid.1);
        }
    }

    // XXX if we dump all results in a trie first we can then
    // output them nicely in order of the file tree ?
    Ok(())
}


#[derive(Parser)]
#[command(author, version)]
#[command(propagate_version=true)]
struct Cli {
        #[command(subcommand)]
        command: Commands,
        
        #[arg(short, long, action = clap::ArgAction::Count)]
        verbose: u8,

        #[arg(long, global=true, help="Database file to use")]
        db: Option<String>,
}

#[derive(Subcommand)]
enum Commands {
    /// Calculate permissions
    Calc_Perms {
        #[arg(long, help="Username to calculate permissions for")]
        user: String,
        #[arg(long, help="Write resulting database to filename <OUTPUT>")]
        output: Option<String>
    },
    /// Compare two database and output the differences between them
    Compare {
        #[arg(long, help="Old database to compare against")]
        old_db: String
    },    
    /// Filter path tree with regular expressions
    Filter {
        #[arg(long, help="Regular expression to filter path tree")]
        filter: String,
    },
    /// Index one or more directories into a database file
    Index {
        #[arg(long, help="Paths that need to be indexed")]
        paths: Vec<String>
    },
    /// List children of the provided path
    List_Paths {
        #[arg(long)]
        needle: String,
        #[arg(long, default_value_t = false)]
        show_hidden: bool
    },
    /// List uids and usernames in this database file
    List_Users {
    }
}

fn main() -> Result<()> {  
    let cli = Cli::parse();

    let level = match &cli.verbose {
        3 => "debug",
        2 => "info",
        1 => "warn",
        0 => "error",
        _ => "trace"
    };
    /* only overrid env if -v is specified else rely on env being set externally */
    if cli.verbose != 0 {
        env::set_var("RUST_LOG", level);
    }
    env_logger::init();

    let db = match &cli.db {
        None => {
            return Err(anyhow!("Needs a --db argument"));
        },
        Some(e) => e
    };

    match &cli.command {
        Commands::Calc_Perms{user, output} => {
            let idb = db_read(&PathBuf::from(db))?;
            let new_db = idb.calculate_permissions(user)?;
            match output {
                None => {
                    for entry in new_db.iter() {
                        println!("{} {}", entry.flags, entry);
                    }
                },
                Some(outputfn) => {
                    if db == outputfn {
                        return Err(anyhow!("Output file cannot be the same as input file"));
                    }
                    db_write(&PathBuf::from(outputfn), &new_db)?;
                }
            }
            Ok(())
        },
        Commands::Compare{old_db} => {
            let old_db = db_read(&PathBuf::from(old_db))?;
            let new_db = db_read(&PathBuf::from(db))?;
            compare(&old_db, &new_db)
        },
        Commands::Filter{filter} => {
            let db = db_read(&PathBuf::from(db))?;
            let new_db = db.filter(filter)?;
            for entry in new_db.iter() {
                println!("{}", entry);
            }
            Ok(())
        },
        Commands::Index{paths} => {
            let mut paths = paths.clone();
            create_index(&db, &mut paths)
        },
        Commands::List_Paths{needle, show_hidden} => {
            let db = db_read(&PathBuf::from(db))?;
            for chld in db.path_children(needle, *show_hidden) {
                println!("{}", chld);
            }
            Ok(())
        },
        Commands::List_Users{} => {
            let db = db_read(&PathBuf::from(db))?;
            for user in db.list_users() {
                println!("{0} ({1})", user.name, user.uid);
            }
            Ok(())
        },
    }?;

    Ok(())
}
