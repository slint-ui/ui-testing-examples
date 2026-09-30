use std::rc::Rc;

use slint::{Model, ModelRc, VecModel};

slint::include_modules!();

fn update_summary(app: &AppWindow, todos: &VecModel<TodoItem>) {
    let remaining = todos.iter().filter(|todo| !todo.done).count();
    app.set_remaining(remaining as i32);
    app.set_has_completed(remaining < todos.row_count());
}

fn main() -> Result<(), slint::PlatformError> {
    let app = AppWindow::new()?;

    let todos = Rc::new(VecModel::from(vec![
        TodoItem {
            title: "Install Slint".into(),
            done: true,
        },
        TodoItem {
            title: "Write a UI test".into(),
            done: false,
        },
    ]));
    app.set_todos(ModelRc::from(todos.clone()));
    update_summary(&app, &todos);

    app.on_add_todo({
        let app = app.as_weak();
        let todos = todos.clone();
        move |title| {
            todos.push(TodoItem { title, done: false });
            update_summary(&app.unwrap(), &todos);
        }
    });

    app.on_todo_toggled({
        let app = app.as_weak();
        let todos = todos.clone();
        move |index, done| {
            let index = index as usize;
            if let Some(mut todo) = todos.row_data(index) {
                todo.done = done;
                todos.set_row_data(index, todo);
            }
            update_summary(&app.unwrap(), &todos);
        }
    });

    app.on_clear_completed({
        let app = app.as_weak();
        let todos = todos.clone();
        move || {
            let open: Vec<TodoItem> = todos.iter().filter(|todo| !todo.done).collect();
            todos.set_vec(open);
            update_summary(&app.unwrap(), &todos);
        }
    });

    app.run()
}
