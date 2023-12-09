use std::env;
use std::fs;

fn parse_input(path: &str) -> Option<Vec<(String, i32)>> {
    fs::read_to_string(path).ok()?
    .lines().map(|line| {
        let mut tokens = line.split(' ');
        let hand = tokens.next()?.to_string();
        let bid = tokens.next()?.parse().ok()?;
        Some((hand, bid))
    }).collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    assert_eq!(args.len(), 2, "no command line arguments provided");
    println!("{:?}", parse_input(&args[1]).unwrap());
}
