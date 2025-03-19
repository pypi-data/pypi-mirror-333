use anyhow::{anyhow, Result};
use std::fmt;
use core::fmt::{Display, Formatter};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{Read, Write};
use std::path::{PathBuf, Path};
use fst::{Map, Streamer, IntoStreamer, MapBuilder};
use regex_automata::dense;
use std::collections::{HashMap};

use radix_trie::{Trie, TrieCommon};
use nix::sys::stat::{Mode, SFlag};
use bitflags::bitflags;
use zip::write::FileOptions;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Mappings {
    pub uidmap: HashMap<u32, u16>,
    pub gidmap: HashMap<u32, u16>,
    pub uidnamemap: HashMap<u32, String>,
    pub gidnamemap: HashMap<u32, Vec<String>>,
}

impl Mappings {

    pub fn uid_mapback(&self, mapped_uid: u16) -> Result<u32> {
        for (k, v) in &self.uidmap {
            if *v == mapped_uid {
                return Ok(*k);
            }
        }
        Err(anyhow!("cannot map uid {mapped_uid} back"))
    }

    pub fn gid_mapback(&self, mapped_gid: u16) -> Result<u32> {
        for (k, v) in &self.gidmap {
            if *v == mapped_gid {
                return Ok(*k);
            }
        }
        Err(anyhow!("cannot map gid {mapped_gid} back"))
    }

    pub fn uid_mapback_incl_username(&self, mapped_uid: u16) -> (u32, String) {
        for (k, v) in &self.uidmap {
            if *v == mapped_uid {
                return match self.uidnamemap.get(k) {
                    Some(e) => (*k, e.to_string()),
                    None => (*k, format!("{k}"))
                };
            }
        }
        panic!("cannot map uid {mapped_uid} back");
    }

    pub fn gid_mapback_incl_username(&self, mapped_gid: u16) -> (u32, String) {
        for (k, v) in &self.gidmap {
            if *v == mapped_gid {
                return match self.gidnamemap.get(k) {
                    Some(e) => (*k, 
                        match e.len() {
                            0 => format!("{k}"),
                            _ => e[0].to_string()
                        }),
                    None => (*k, format!("{k}"))
                };
            }
        }
        panic!("cannot map gid {mapped_gid} back");
    }

    pub fn username_to_uid(&self, username: &str) -> Result<u32> {
        for (k, v) in &self.uidnamemap {
            if v == username {
                return Ok(*k);
            }
        }
        Err(anyhow!("cannot map {username} back to uid"))
    }

    pub fn uid_to_username(&self, uid: u32) -> Result<String> {
        match &self.uidnamemap.get(&uid) {
            Some(u) => Ok(u.to_string()),
            None => Err(anyhow!("cannot map uid {uid} to username"))
        }
    }

    pub fn get_gids_for_uid(&self, uid: u32) -> Result<Vec<u32>> {
        let mut ret = Vec::new();
        let username = self.uid_to_username(uid)?;
        for (k, v) in &self.gidnamemap {
            if v.contains(&username) {
                ret.push(*k);
            }
        }
        Ok(ret)
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Meta {
    pub pathcount: u64,
    pub dirnames: Vec<String>,
    pub annotated: Option<bool>
}

pub struct Db {
    pub mappings: Mappings,
    pub fst: Map<Vec<u8>>,
    pub meta: Meta,
}

#[derive(Debug)]
pub struct User {
    pub name: String,
    pub uid: u32
}

#[derive(Debug)]
pub struct PathEntry {
    pub path: String,
    pub flags: Flags
}

bitflags! {
    #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
    pub struct Flags: u32 {
        const EMPTY = 0b0;
        const CAN_EXEC =  0b00000001;
        const CAN_READ =  0b00000010;
        const CAN_WRITE = 0b00000100;
        const HAS_SUBDIR_EXEC =  0b00001000;
        const HAS_SUBDIR_READ =  0b00010000;
        const HAS_SUBDIR_WRITE = 0b00100000;
        const IS_SYMLINK = 0b001000000;
        const IS_IGNORED = 0b010000000;
        const IS_SOCKET = 0b100000000;
    }
}

impl Flags {
    pub fn as_u32(&self) -> u32 {
        self.bits() as u32
    }
    pub fn to_string(&self) -> String {
        let mut ret = String::new();
        if self.contains(Flags::IS_IGNORED) {
            ret.push_str("ign ---");
            return ret;
        }
        if self.contains(Flags::IS_SOCKET) {
            ret.push_str("s--");
        }
        else {
            if self.contains(Flags::HAS_SUBDIR_READ) { ret.push('R') } else { ret.push('-') };
            if self.contains(Flags::HAS_SUBDIR_WRITE) { ret.push('W') } else { ret.push('-') };
            if self.contains(Flags::HAS_SUBDIR_EXEC) { ret.push('X') } else { ret.push('-') };
        }
        ret.push(' ');
        if self.contains(Flags::IS_SYMLINK) {
            ret.push_str("l--");
        }
        else {
            if self.contains(Flags::CAN_READ) { ret.push('r') } else { ret.push('-') };
            if self.contains(Flags::CAN_WRITE) { ret.push('w') } else { ret.push('-') };
            if self.contains(Flags::CAN_EXEC) { ret.push('x') } else { ret.push('-') };
        }
        ret
    }
}

pub fn db_write(dbfilename: &PathBuf, db: &Db) -> Result<()> {

    let file = std::fs::File::create(dbfilename)?;
    let mut archive = zip::ZipWriter::new(file);
    archive.start_file("fst", FileOptions::default())?;

    archive.write_all(&db.fst.as_fst().as_bytes())?;

    archive.start_file("mappings", FileOptions::default())?;
    serde_json::to_writer(archive.by_ref(), &db.mappings)?;

    archive.start_file("meta", FileOptions::default())?;
    serde_json::to_writer(archive.by_ref(), &db.meta)?;

    Ok(())
}

pub fn db_read(dbfilename: &PathBuf) -> Result<Db> {
        let dbfile = File::open(dbfilename)?;
        let mut archive = zip::ZipArchive::new(dbfile)?;

        let file = archive.by_name("mappings")?;
        let mappings: Mappings = serde_json::from_reader(file)?;

        log::trace!("Mappings {:?}", mappings);

        let file = archive.by_name("meta")?;
        let meta: Meta = serde_json::from_reader(file)?;

        // we could improve memory usage by writing the FST to a temp
        // file and then mmapping it
        let mut file = archive.by_name("fst")?;
        let mut buffer = Vec::new();
        file.read_to_end(&mut buffer)?;
        let fst = fst::Map::new(buffer)?;      

        Ok(Db {
            mappings: mappings,
            fst: fst,
            meta: meta,
        })
}

#[inline(always)]
pub fn map_uxpermvalue(mode: u32, uid: u16, gid: u16) -> u64 {
    (mode as u64) | ((uid as u64) << 32) | ((gid as u64) << 48)
}

#[inline(always)]
pub fn unmap_uxpermvalue(value: u64) -> (u32, u16, u16) {
    let mode = (value & 0xffff) as u32;
    let uid = ((value >> 32) & 0xffff) as u16;

    /* this looks weird but we clear the top bit as that would signal
     * an ignored path and not a gid; we sitll have room for 32767
     * gids */
    let gid = ((value >> 48) & !(1 << 15)) as u16;
    (mode, uid, gid)
}

#[inline(always)]
fn is_ignored(value: u64) -> bool {
    ((value >> 63) & 1) == 1
}

#[inline(always)]
fn can_execute(pmode: u32, puid: u32, pgid: u32, uid: u32, gids: &Vec<u32>) -> bool {
    (puid == uid && ((pmode & Mode::S_IXUSR.bits()) != 0)) ||
        (gids.contains(&pgid) && ((pmode & Mode::S_IXGRP.bits()) != 0)) ||
        ((pmode & Mode::S_IXOTH.bits()) != 0)
}

#[inline(always)]
fn can_write(pmode: u32, puid: u32, pgid: u32, uid: u32, gids: &Vec<u32>) -> bool {
    (puid == uid && ((pmode & Mode::S_IWUSR.bits()) != 0)) ||
        (gids.contains(&pgid) && ((pmode & Mode::S_IWGRP.bits()) != 0)) ||
        ((pmode & Mode::S_IWOTH.bits()) != 0) ||
        (uid == 0)
}

#[inline(always)]
fn can_read(pmode: u32, puid: u32, pgid: u32, uid: u32, gids: &Vec<u32>) -> bool {
    (puid == uid && ((pmode & Mode::S_IRUSR.bits()) != 0)) ||
        (gids.contains(&pgid) && ((pmode & Mode::S_IRGRP.bits()) != 0)) ||
        ((pmode & Mode::S_IROTH.bits()) != 0) ||
        (uid == 0)
}

#[cfg(not(target_os="windows"))]
#[inline(always)]
fn get_regexp_pattern(path: &str, show_hidden: bool, dirs_only: bool) -> String {
    /* XXX: maybe use lazy_static! to initialize the string constants so we
     * don't have to do the conversion every time we call this function */
    let mut parts = Vec::new();

    /* start with the path we want to find children of */
    let escaped_path = regex::escape(path);
    parts.push(escaped_path.clone());

    /* add the path separator if needed */
    if escaped_path.len() > 1 || (escaped_path.len() == 1 && !escaped_path.starts_with('/')) {
        parts.push("/".to_string());
    }

    /* filter out entries starting with a period (.) if asked to do so */
    if !show_hidden {
        parts.push("[^/.]+".to_string());
    }

    /* match child entries just one level deep */
    parts.push("[^/]+".to_string());

    if dirs_only {
        parts.push("[/]".to_string())
    }

    parts.join("")
}

#[inline(always)]
fn get_regexp_pattern_for_dirs(path: &str, show_hidden: bool) -> String {
    get_regexp_pattern(path, show_hidden, true)
}

#[inline(always)]
fn get_regexp_pattern_for_files(path: &str, show_hidden: bool) -> String {
    get_regexp_pattern(path, show_hidden, false)
}

impl Db {

    pub fn common_prefix_path(&self) -> String {
        /* XXX: we could calculate it upon loading of the database or at least cache it? */
        let mut paths: Vec<&Path> = Vec::new();

        for dirname in &self.meta.dirnames {
            paths.push(Path::new(dirname));
        }

        let prefix = common_path::common_path_all(paths).unwrap();
        prefix.into_os_string().into_string().unwrap()
    }

    pub fn is_annotated(&self) -> bool {
        match self.meta.annotated {
            None => false,
            Some(e) => e
        }
    }

    pub fn path_children(&self, path: &str, show_hidden: bool) -> Vec<PathEntry> {
        let mut children: Vec<PathEntry> = Vec::new();
        log::debug!("finding children of {path} (show_hidden: {show_hidden})");

        /* find the subdirectories of path */
        let pattern = get_regexp_pattern_for_dirs(path, show_hidden);
        log::trace!("regexp dir pattern: {pattern}");
        let dfa = dense::Builder::new().anchored(true).build(&pattern).unwrap();
        let mut stream = self.fst.search(&dfa).into_stream();
        while let Some(v) = stream.next() {
            children.push(
                PathEntry {
                    path: String::from_utf8(v.0.to_vec()).unwrap(),
                    flags: Flags::from_bits_retain(v.1.try_into().unwrap())
                }
            );
        }

        /* find the files that are in this path */
        let pattern = get_regexp_pattern_for_files(path, show_hidden);
        log::trace!("regexp file pattern: {pattern}");
        let dfa = dense::Builder::new().anchored(true).build(&pattern).unwrap();
        let mut stream = self.fst.search(&dfa).into_stream();
        while let Some(v) = stream.next() {
            children.push(
                PathEntry {
                    path: String::from_utf8(v.0.to_vec()).unwrap(),
                    flags: Flags::from_bits_retain(v.1.try_into().unwrap())
                }
            );
        }

        children
    }

    pub fn calculate_permissions(&self, user: &str) -> Result<Db> {
        let uid = self.mappings.username_to_uid(user)?;
        let gids = self.mappings.get_gids_for_uid(uid)?;
        log::debug!("uid: {}, gids: {:?}", uid, gids);

        let mut trie: Trie<String, Flags> = Trie::new();

        let mut stream = self.fst.into_stream();

        /* the first of the dirnames is what we set as the current directory */
        let dirname = &self.meta.dirnames[0];
        let mut nd = dirname.clone();
        if !(nd.len() == 1 && nd.starts_with('/')) {
            nd.push('/');
        }
        let curdir = Path::new(&nd).to_path_buf();

        let mut pathcount: u64 = 0;

        while let Some(v) = stream.next() {
            let pathname = String::from_utf8(v.0.to_vec()).unwrap();
            let pathbuf = Path::new(&pathname).to_path_buf();
            let parent_curdir = curdir.parent();

            let is_ignored = is_ignored(v.1);
            let (pmode, muid, mgid) = unmap_uxpermvalue(v.1);

            let puid = self.mappings.uid_mapback(muid)?;
            let pgid = self.mappings.gid_mapback(mgid)?;

            let can_exec = can_execute(pmode, puid, pgid, uid, &gids);
            let can_read = can_read(pmode, puid, pgid, uid, &gids);
            let can_write = can_write(pmode, puid, pgid, uid, &gids);

            let is_symlink = pmode & SFlag::S_IFMT.bits() == SFlag::S_IFLNK.bits();
            let is_socket = pmode & SFlag::S_IFMT.bits() == SFlag::S_IFSOCK.bits();

            let mut first = true;

            for p in pathbuf.ancestors() {

                let mut strp = p.to_str().unwrap().to_string();
                if !first && !strp.ends_with('/') {
                    strp.push('/');
                }

                let mut path_value = match trie.get(&strp) {
                    Some(o) => *o,
                    None => Flags::EMPTY,
                };

                if !first || p.is_dir() {
                    if !is_symlink && path_value.contains(Flags::CAN_EXEC) {
                        if can_exec {
                            path_value |= Flags::HAS_SUBDIR_EXEC;
                        }
                        if can_read {
                            path_value |= Flags::HAS_SUBDIR_READ;
                        }
                        if can_write {
                            path_value |= Flags::HAS_SUBDIR_WRITE;
                        }
                    }
                }

                if first {
                    if is_ignored {
                        path_value |= Flags::IS_IGNORED;
                        log::trace!("ignored path found: {}", strp);
                    }
                    if is_symlink {
                        path_value |= Flags::IS_SYMLINK;
                    }
                    if is_socket {
                        path_value |= Flags::IS_SOCKET;
                    }
                    if !is_symlink {
                        if can_exec {
                            path_value |= Flags::CAN_EXEC;
                        }
                        if can_read {
                            path_value |= Flags::CAN_READ;
                        }
                        if can_write {
                            path_value |= Flags::CAN_WRITE;
                        }
                    }
                }

                if first {
                    first = false;
                }

                log::trace!("inserted {} with value {}", strp, path_value);
                trie.insert(strp, path_value);
            }

            pathcount += 1;
        }

        let mut pathfst_builder = MapBuilder::memory();
        for v in trie.iter() {
            let pathname = v.0;
            let flags = *v.1;
            pathfst_builder.insert(pathname, flags.as_u32().into())?;
        }

        let mappings = self.mappings.clone();
        let mut meta = self.meta.clone();
        meta.annotated = Some(true);
        assert!(meta.pathcount == pathcount, "meta.pathcount = {}, pathcount = {}", meta.pathcount, pathcount);

        let fst = fst::Map::new(pathfst_builder.into_inner()?)?;
        Ok(Db {
            mappings: mappings,
            fst: fst,
            meta: meta,
        })
    }

    pub fn filter(&self, filter: &str) -> Result<Db> {
        let dfa = dense::Builder::new().anchored(true).build(&filter);
        if !dfa.is_ok() {
            log::error!("Invalid regular expression supplied for path");
            return Err(anyhow!("The filter regular expression is invalid"));
        }
        let dfa = dfa.unwrap();

        let mut stream = self.fst.search(&dfa).into_stream();

        let mut pathfst_builder = MapBuilder::memory();
        let mut pathcount: u64 = 0;

        /*
         * Rewriting dirnames is going to be a massive pain in the ass
         * given that the regexp will just match full paths; which means we
         * will not get the intermediate paths which then obviously is an issue
         *
         * lets say original indexing was for / and then we filter and result 
         * on /home/gvb/python/ and /home/gvb/rust, we will be missing the /home/
         * and /home/gvb/ entries.
         *
         * if we loop through it we can add the directories if they're not in a
         * cache already which means that for each result we must parse the basepath
         * and figure out if it, or one if its parents, is already in the cache
         * and use that to ultimately build up dirnames; we then need to rewrite
         * the FST again to insert these dirnames in the right spot to be able
         * to get a proper function Db that works with the current way path_children()
         * works.
         *
         * AAAAAAARRRRGGGGHHH
         *
         * another option is to use a Trie as an intermediate structure as there
         * we dont need to insert in lexicographic order; we can do two things; have
         * a different return type where we simply return the trie that is then
         * being used for searching however that would lose all the awesome FST
         * type stuff such as the regexps etc that we can then use
         *
         * so maybe we should use the trie as an intermediate structure, and then
         * after that use that to build up the FST?
         *
         * AAAAAAAAAAAAARGGH
         *
         * another option is to have a separate structure inside the Db for this
         * filtered case and take that into account when listing children, which
         * means we need to take two paths when listing chlidren, the normal one
         * and the other one that does the other directories for intermediate stuff;
         * with a lot of results that becomes painful too as we would need to
         * cache them internally and then sort them as that is the expected
         * behavior of the calling client; and we would have to do that upon
         * every listing; so it is better to build up a structure that has this
         * data in the right way from the get-go
         *
         * in the end I decided to use a trie.
         */

        let mut trie = Trie::new();

        while let Some(v) = stream.next() {
            let s = String::from_utf8(v.0.to_vec()).unwrap();
            let mut p = Path::new(&s);

            while p.parent().is_some() {
                p = p.parent().unwrap();
                let mut b = p.to_path_buf().into_os_string().into_string().unwrap();
                if trie.get(&b).is_none() {
                    if !(b.len() == 1 && b.starts_with("/")) {
                        b.push_str("/");
                        match self.fst.get(b.clone()) {
                            None => break,
                            Some(fstval) => {
                                trie.insert(b.clone(), fstval);
                            }
                        }
                    }
                }

                /* break if this is part of original set of dirnames, no need to
                 * create entries for above and beyond then */
                if self.meta.dirnames.contains(&b) {
                    break;
                }
            }
            pathcount = pathcount + 1;
            trie.insert(s.clone(), v.1);
        }

        for v in trie.iter() {
            pathfst_builder.insert(v.0, *v.1)?;
        }

        let mappings = self.mappings.clone();
        let mut meta = self.meta.clone();
        meta.pathcount = pathcount;

        let fst = fst::Map::new(pathfst_builder.into_inner()?)?;

        Ok(Db {
            mappings: mappings,
            fst: fst,
            meta: meta,
        })
    }

    pub fn list_users(&self) -> Vec<User> {
        let mut ret = Vec::new();
        for (uid, name) in &self.mappings.uidnamemap {
            ret.push(User { name: name.to_string(), uid: *uid });
        }
        ret.sort_by_key(|d| d.name.clone());
        ret
    }

    pub fn iter(&self) -> DbIntoIterator {
        let stream = self.fst.into_stream();
        DbIntoIterator {
            stream: stream
        }
    }
}

pub struct DbIntoIterator<'a> {
    stream: fst::map::Stream<'a>
}

impl Iterator for DbIntoIterator<'_> {
    type Item = PathEntry;
    fn next(&mut self) -> Option<PathEntry> {
        match self.stream.next() {
            Some(v) => {
                Some(PathEntry {
                    path: String::from_utf8(v.0.to_vec()).unwrap(),
                    flags: Flags::from_bits_retain(v.1.try_into().unwrap())
                })
            },
            None => None
        }
    }
}

impl Display for PathEntry {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.path)
    }
}

impl Display for Flags {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

#[test]
fn test_uxperm() {
    assert_eq!(unmap_uxpermvalue(map_uxpermvalue(0xf0f0, 255, 255)), (0xf0f0, 255,255));
    assert_eq!(unmap_uxpermvalue(map_uxpermvalue(0xf0f0, 345, 890)), (0xf0f0, 345,890));
    assert_eq!(unmap_uxpermvalue(map_uxpermvalue(0xf0f0, 256, 256)), (0xf0f0, 256,256));
}
