use anyhow::{anyhow, Result};
use std::process::Command;

pub fn uid_to_name(uid: u32) -> Result<String> {
    let output = Command::new("getent")
        .arg("passwd")
        .arg(uid.to_string())
        .output()?;
    if !output.status.success() {
        return Err(anyhow!("getent passwd failed"));
    }
    let output = String::from_utf8(output.stdout)?;
    log::trace!("getent passwd {} -> {}", uid, output);
    let line = output.lines().next().unwrap().to_string();
    Ok(line.split(":").next().unwrap().to_string())
}

pub fn gid_to_name(uid: u32) -> Result<(String, Vec<String>)> {
    let output = Command::new("getent") .arg("group") .arg(uid.to_string()) .output()?;
    if !output.status.success() {
        return Err(anyhow!("getent group failed"));
    }
    let output = String::from_utf8(output.stdout)?;
    log::trace!("getent group {} -> {}", uid, output);
    let line = output.lines().next().unwrap().to_string();
    let parts: Vec<_> = line.split(":").collect();
    if parts.len() < 4 {
        return Err(anyhow!("getent group returned invalid"));
    }
    let usernames: Vec<_> = parts[3].split_terminator(",").map(|x| x.to_string()).collect();
    Ok((parts[0].to_string(), usernames))
}
