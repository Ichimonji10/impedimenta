pub fn add_two(x: i32) -> i32 {
    x + 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(add_two(-3), -1);
        assert_eq!(add_two(-2), 0);
        assert_eq!(add_two(-1), 1);
        assert_eq!(add_two(0), 2);
        assert_eq!(add_two(1), 3);
        assert_eq!(add_two(-3), -1);
    }
}
