use std::env;
use std::error::Error;
use std::fs;

pub struct Config {
    pub query: String,
    pub filename: String,
    pub case_sensitive: bool,
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &'static str> {
        let nargs = 3;
        if args.len() < nargs {
            return Err("not enough arguments");
        } else if args.len() > nargs {
            return Err("too many arguments");
        }

        // NOTE: CASE_INSENSITIVE is confusing, as users need to think about
        // double negatives. CASE_SENSITIVE would be more straightforward.
        let query = args[1].to_string();
        let filename = args[2].to_string();
        let case_sensitive = env::var("CASE_INSENSITIVE").is_err();
        Ok(Config { query, filename, case_sensitive })
    }
}

pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let contents = fs::read_to_string(config.filename)?;
    let lines = if config.case_sensitive {
        search_case_sensitive(&config.query, &contents)
    } else {
        search_case_insensitive(&config.query, &contents)
    };
    for line in lines {
        println!("{}", line);
    }
    Ok(())
}

pub fn search_case_sensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = vec![];
    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }
    results
}

pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = vec![];
    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }
    results
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_new_0_args() {
        let args: Vec<String> = vec![];
        match Config::new(&args) {
            Ok(_) => panic!(),
            Err(_) => (),
        }
    }

    #[test]
    fn test_config_new_1_args() {
        let args: Vec<String> = vec!["path/to/bin".to_string()];
        match Config::new(&args) {
            Ok(_) => panic!(),
            Err(_) => (),
        }
    }

    #[test]
    fn test_config_new_2_args() {
        let args: Vec<String> = vec!["path/to/bin".to_string(), "needle".to_string()];
        match Config::new(&args) {
            Ok(_) => panic!(),
            Err(_) => (),
        }
    }

    #[test]
    fn test_config_new_3_args() {
        let args: Vec<String> = vec![
            "path/to/bin".to_string(),
            "needle".to_string(),
            "haystack".to_string(),
        ];
        let config = Config::new(&args).unwrap();
        assert_eq!(config.query, args[1].to_string());
        assert_eq!(config.filename, args[2].to_string());
    }

    #[test]
    fn test_config_new_4_args() {
        let args: Vec<String> = vec![
            "path/to/bin".to_string(),
            "needle".to_string(),
            "haystack".to_string(),
            "extra".to_string(),
        ];
        match Config::new(&args) {
            Ok(_) => panic!(),
            Err(_) => (),
        }
    }

    #[test]
    fn test_search_0_results() {
        let query = "rust";
        let contents = "
Rust:
safe, fast, productive.
Pick three.";
        let actual = search_case_sensitive(query, contents);
        let target: Vec<&str> = vec![];
        assert_eq!(actual, target);
    }

    #[test]
    fn test_search_1_result() {
        let query = "Rust";
        let contents = "
Rust:
safe, fast, productive.
Pick three.";
        let actual = search_case_sensitive(query, contents);
        let target = vec!["Rust:"];
        assert_eq!(actual, target);
    }

    #[test]
    fn test_search_2_results() {
        let query = "s";
        let contents = "
Rust:
safe, fast, productive.
Pick three.";
        let actual = search_case_sensitive(query, contents);
        let target = vec!["Rust:", "safe, fast, productive."];
        assert_eq!(actual, target);
    }

    #[test]
    fn test_search_case_insensitive() {
        let query = "ruST";
        let contents = "
Rust:
safe, fast, productive.
Pick three.";
        let actual = search_case_insensitive(query, contents);
        let target = vec!["Rust:"];
        assert_eq!(actual, target);
    }
}
