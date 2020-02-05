#![feature(proc_macro_hygiene, decl_macro, plugin)]

#[macro_use]
extern crate rocket;
#[macro_use]
extern crate serde_derive;
extern crate rocket_contrib;
extern crate serde_json;

use rocket::response::content;
use rocket_contrib::serve::StaticFiles;
use rocket_contrib::templates::Template;
// use serde_json::json;
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize)]
struct Entry {
    id: u8,
    title: String,
    body: String,
}

#[get("/")]
fn home() -> Template {
    let context = HashMap::<String, String>::new();
    Template::render("home", &context)
}

#[get("/about")]
fn about() -> Template {
    let context = HashMap::<String, String>::new();
    Template::render("about", &context)
}
#[get("/entries/<id>")]
fn get(id: u8) -> Template {
    let title = String::from("This is my First Post!");
    let body = String::from("This is something something a post or somet5hing rather idk.");
    let context = Entry { id, title, body };
    Template::render("post", &context)
}

fn rocket() -> rocket::Rocket {
    rocket::ignite()
        .mount("/", routes![home, get, about])
        .mount("/public", StaticFiles::from("/static"))
        .attach(Template::fairing())
}

#[catch(404)]
fn not_found(req: &rocket::Request) -> content::Html<String> {
    content::Html(format!(
        "<p>Sorry, but '{} is not a valid path!</p>",
        req.uri()
    ))
}

fn main() {
    rocket().launch();
}
