use std::collections::HashMap;
use std::io;
use csv::{Reader, Writer};
use chrono::{Local, DateTime, Datelike};
use std::{
    env,
    error::Error,
    ffi::OsString,
    fs::{File, OpenOptions},
    process,
};

struct Day {
    available_time: f32;
    next_day: &str;
}

impl Day {
    fn new(time: f32, next: &str) -> Day {
        Day {
            available_time: time, 
            next_day: next,
        }
    }
}

static file_path: &str = "/home/jjl20011/snap/snapd-desktop-integration/current/Lab/Rust-Learning/Rust_Min_Lateness_Scheduling/Rust_Scheduler/resources/assignment_schedule.csv";

/// get all of the assignments as command line input
/// until termination
/// 
/// Arguments
/// - None
/// 
/// Returns
/// - None
fn get_assignments() {
    
    let mut user_input = String::new();
    while user_input != "stop" {
        let input_vector = 
        io::stdin.read_line(&mut user_input).expect("failed to read line");
    }
}

/// Builds a HashMap which can be used to cite the 
/// hours available for work on each day. 
/// 
/// Arguments: 
/// - None
/// 
/// Returns
/// - date_time_alloc --- HashMap storing the days of the 
/// week as keys and their respective available times as values
/// 
/// The cumulative available time is as follows:
/// Sunday: 1-8 (-1) -> 1-7
/// Monday: 8-15
/// Tuesday: 16-22
/// Wednesday: 23-28
/// Thursday: 29-32
/// Friday: 33-39
/// Saturday: 40-47
fn build_day_alloc() -> HashMap<&'static str, i32> {
    let mut date_time_alloc = HashMap::new();
    date_time_alloc.insert("Sun", Day::new(7, "Mon"));
    date_time_alloc.insert("Mon", Day::new(7, "Tue"));
    date_time_alloc.insert("Tue", Day::new(4, "Wed"));
    date_time_alloc.insert("Wed", Day::new(6, "Thu"));
    date_time_alloc.insert("Thu", Day::new(4, "Fri"));
    date_time_alloc.insert("Fri", Day::new(7, "Sat"));
    date_time_alloc.insert("Sat", Day::new(8, "Sun"));

    return date_time_alloc;
}

fn main() -> Result<(), Box<dyn Error>> {
    
    let date_time_alloc = build_day_alloc();

    let now: DateTime<Local> = Local::now();
    println!("Current date and time: {}", now);

    let mut schedule_records = Vec::new();
    // need to set all of the file options in order for this to work properly
    let file = OpenOptions::new().read(true).write(true).append(true).open(file_path).unwrap();

    let mut rdr = Reader::from_reader(&file);
    for result in rdr.records() {
        schedule_records.push(result)
    }
    
    if schedule_records.len() == 0 {
        let mut writer = Writer::from_writer(file);
        let new_date = format!("{}", now);
        println!("No records have been added. No previous update");
        writer.write_record(&[new_date]).unwrap();
        writer.flush().unwrap();
    }

    let current_day = format!("{}", now.weekday());

    Ok(())

}

// Program Steps: 
// 1. Read the csv data from the resources folder
//      - check last date, if there exists one, otherwise, write the current date as 
//      the last update time
//      - check the day of the last updated day. 
//      - Read all of the current tasks into scope of the program
//      - If there are any tasks in the queue, ask the user to check off any which 
//      have been completed. 
//      - Get the new date, and subtract from their deadline the amount of time which
//      has passed between the previous check date and the current date
// 2. Read new tasks into the program scope
//      - rerun the algorithm and save the new set of dates to the csv resources data

// Check the local time + date
// ----------------------------
// use chrono::{Utc, DateTime};
// 
// let date_string = "2020-05-15T08:00:00Z"; // replace this with your date string
// let date_time: DateTime<Utc> = date_string.parse().unwrap();
// println!("{}", date_time);