type Hand = [u32; 5];
type Hands = Vec<(Hand, i32)>;

#[derive(PartialEq, Eq, PartialOrd, Ord)]
enum HandType {
    HighCard,
    OnePair,
    TwoPair,
    ThreeKind,
    FullHouse,
    FourKind,
    FiveKind
}

fn to_index(c: char) -> u32 {
    match c {
        'A' => 12,
        'K' => 11,
        'Q' => 10,
        'J' => 9,
        'T' => 8,
        _ => c.to_digit(10).unwrap() - 2
    }
}

fn parse_input(path: &str) -> Option<Hands> {
    use std::convert::TryInto;
    std::fs::read_to_string(path).ok()?
    .lines().map(|line| {
        let (hand_tok, bid_tok) = line.split_once(' ')?;
        let hand = hand_tok.chars().map(|c| to_index(c))
            .collect::<Vec<_>>().try_into().ok()?;
        let bid = bid_tok.parse().ok()?;
        Some((hand, bid))
    }).collect()
}

fn to_handtype(hand: &Hand) -> HandType {
    let mut card_count = vec![0; 13];
    for card in hand {
        card_count[*card as usize] += 1;
    }
    let mut seen_five = false;
    let mut seen_four = false;
    let mut seen_three = false;
    let mut seen_two = 0;
    for count in card_count {
        match count {
            5 => {
                seen_five = true;
            },
            4 => {
                seen_four = true;
            },
            3 => {
                seen_three = true;
            },
            2 => {
                seen_two += 1;
            }
            _ => ()
        }
    }
    if seen_five {
        HandType::FiveKind
    } else if seen_four {
        HandType::FourKind
    } else if seen_three && seen_two == 1 {
        HandType::FullHouse
    } else if seen_three {
        HandType::ThreeKind
    } else if seen_two == 2 {
        HandType::TwoPair
    } else if seen_two == 1 {
        HandType::OnePair
    } else {
        HandType::HighCard
    }
}

fn compare_hands(a: &Hand, b: &Hand) -> std::cmp::Ordering {
    let ah = to_handtype(a);
    let bh = to_handtype(b);
    if ah == bh {
        for (ac, bc) in a.iter().zip(b.iter()) {
            if ac != bc {
                return ac.cmp(bc)
            }
        }
        std::cmp::Ordering::Equal
    } else {
        ah.cmp(&bh)
    }
}

fn problem1(mut hands: Hands) -> i32 {
    hands.sort_unstable_by(|a, b| compare_hands(&a.0, &b.0));
    let mut sum = 0;
    for (index, item) in hands.iter().enumerate() {
        sum += item.1 * ((index as i32) + 1);
    }
    sum
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    assert_eq!(args.len(), 2, "no command line arguments provided");
    println!("{}", problem1(parse_input(&args[1]).unwrap()))
}
