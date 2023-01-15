use crate::ParseError::{InvalidUsage, NoCommand, NotExist, UnacceptableData};
use std::collections::{HashMap, HashSet};
use std::io;

// #[macro_use]
// extern crate prettytable;
use prettytable::{Cell, Row, Table as PTable};

#[derive(Debug)]
enum ParseError {
    NoCommand,
    NotExist,
    InvalidUsage,
    UnacceptableData,
}

struct DamnDB {
    pub tables: HashMap<String, Table>,
}

impl DamnDB {
    pub fn new() -> DamnDB {
        DamnDB {
            tables: HashMap::new(),
        }
    }

    pub fn get_mut(&mut self) -> &mut DamnDB {
        self
    }

    pub fn is_table_exist(&self, table_name: &str) -> bool {
        self.tables.contains_key(table_name)
    }

    pub fn try_create_table(&mut self, table: Table) -> Result<(), &str> {
        if self.is_table_exist(table.name.as_str()) {
            return Err("table with provided name already exists");
        }
        self.tables.insert(table.name.clone(), table);
        Ok(())
    }

    pub fn insert_into_table(&mut self, table_name: &str, data: Vec<String>) -> Result<(), &str> {
        if let Some(table) = self.tables.get_mut(table_name) {
            if table.columns.len() != data.len() {
                return Err("insertion into table more or less than table have columns impossible");
            }
            // let mut indexed_indexes: Option<Vec<usize>> = None;
            // if table.indexed.is_some() {
            //     let v = table.indexed.as_ref().unwrap().keys().into_iter()
            //         .map(|col_indexed_name| table.columns.iter().position(|p| p.eq(col_indexed_name)).unwrap()).collect::<Vec<usize>>();
            //
            //     indexed_indexes = Some(v);
            // }
            let mut it = data.into_iter();
            let leeen = table.data.first().unwrap().len();
            let ddata = &mut table.data;
            for (column_index, x) in ddata.iter_mut().enumerate() {
                //what is indexed? indexed = Option<HashMap<String,HashMap<String, usize>>>
                let col_name = table.columns.get(column_index).unwrap().as_str();
                let val = it.next().unwrap();
                if table.indexed.is_some() && table.indexed.as_mut().unwrap().contains_key(col_name)
                {
                    let b = table.indexed.as_mut().unwrap().get(col_name).unwrap();
                    let mut v: Vec<usize> = Vec::new();
                    if b.get(val.as_str()).is_some() {
                        v = b.get(val.as_str()).unwrap().clone()
                    }
                    v.push(leeen);
                    table
                        .indexed
                        .as_mut()
                        .unwrap()
                        .get_mut(col_name)
                        .unwrap()
                        .insert(val.clone(), v);
                }
                x.push(val);
            }
        } else {
            return Err("insertion into non-existing table impossible");
        }
        Ok(())
    }

    pub fn get_table_mut(&mut self, table_name: &str) -> Result<&mut Table, &str> {
        if let Some(table) = self.tables.get_mut(table_name) {
            Ok(table)
        } else {
            Err("getting into non-existing table impossible")
        }
    }

    pub fn get_table(&self, table_name: &str) -> Result<&Table, &str> {
        if let Some(table) = self.tables.get(table_name) {
            Ok(table)
        } else {
            Err("getting into non-existing table impossible")
        }
    }
}

#[derive(Clone, Debug)]
pub struct Table {
    name: String,
    columns: Vec<String>,
    data: Vec<Vec<String>>,
    indexed: Option<HashMap<String, HashMap<String, Vec<usize>>>>,
    //                      column           value      index
}

impl Table {
    pub fn new(
        name: String,
        columns: Vec<String>,
        data: Vec<Vec<String>>,
        indexed: Option<HashMap<String, HashMap<String, Vec<usize>>>>,
    ) -> Table {
        Table {
            name,
            columns,
            data,
            indexed,
        }
    }
    pub fn print(&self) {
        let mut table = PTable::new();
        table.add_row(Row::new(
            self.columns
                .iter()
                .map(|x| Cell::new(x))
                .collect::<Vec<Cell>>(),
        ));
        if self.data.first().is_some() {
            for row_u in 0..self.data.first().unwrap().len() {
                let mut vvec = Vec::new();
                for column in 0..self.columns.len() {
                    vvec.push(Cell::new(
                        self.data.get(column).unwrap().get(row_u).unwrap().as_str(),
                    ))
                }
                table.add_row(Row::new(vvec));
            }
        }
        table.printstd();
    }

    pub fn add_to_table(&mut self, data: Vec<String>) {
        let mut it = data.into_iter();
        if self.data.is_empty() {
            (0..it.len()).for_each(|_| self.data.push(Vec::new()));
        }
        for x in self.data.iter_mut() {
            x.push(it.next().unwrap());
        }
    }
}

fn main() {
    let mut db = DamnDB::new();
    let vec = vec![
        "create table (first, second);",
        "select from table;",
        "insert table (\"peklo\", \"chortove\");",
        "select from table;",
        "create table2 (third, fouth);",
        "insert into table2 (\"peklo\", \"uuuuh_blin\");",
        "insert into table2 (\"ne_peklo\", \"uuuuh_blina\");",
        "insert table (\"neee_peklo\", \"chortove\");",
        "select from table;",
        "select from table2;",
        "select from table where first = \"neee_peklo\";",
        "select from table full_join table2 on first = third;",
    ];
    vec.into_iter()
        .map(|x| parse_and_execute_command(x, db.get_mut()))
        .take_while(|x| x.is_ok())
        .collect::<Vec<_>>();
    loop {
        let mut cmd_str: String = String::new();
        println!("Enter command");
        //todo change to read until ;
        io::stdin().read_line(&mut cmd_str).unwrap_or_else(|error| {
            println!("oops... we have an error: {:?}", error);
            0
        });
        parse_and_execute_command(cmd_str.as_str(), db.get_mut())
            .unwrap_or_else(|parse_error| println!("oops... we have an error: {:?}", parse_error));
    }
}

fn check_table_name(possible_name: &str) -> bool {
    let mut it = possible_name.chars();
    match it.next() {
        None => false,
        Some(first) => match first.is_ascii_alphabetic() {
            true => it.all(|other| other.is_ascii_alphanumeric()),
            false => false,
        },
    }
}

//unfortunately, architecture of whole of this code sucks, so this function unused
pub fn find_when_inserted_indexed(
    table: &Table,
    column: usize,
    eq_to: &str,
) -> Option<Vec<Vec<String>>> {
    let mut it = table.data.iter();
    let col_name = table.columns.get(column);
    if table.data.is_empty() || table.indexed.is_none() || col_name.is_none() {
        return None;
    }
    let d = table
        .indexed.clone()
        .unwrap();
    let m = d
        .get(col_name.unwrap())
        .unwrap();
    let re = match m.get(eq_to) {
        None => {
            return None;
        }
        Some(veccc) => veccc,
    };
    let mut res = Vec::new();
    for &i in re {
        let mut row = Vec::new();
        for column_i in 0..table.columns.len() {
            row.push(table.data.get(column_i).unwrap().get(i).unwrap().clone());
        }
        res.push(row);
    }
    Some(res)
}

fn parse_and_execute_command(cmd_str: &str, db: &mut DamnDB) -> Result<(), ParseError> {
    let s = cmd_str.trim();
    if s.is_empty() {
        return Err(NoCommand);
    }
    println!("executing order \"{}\"", s);
    // create table_name (first_row, another_row);
    if s.to_lowercase().starts_with("create ") {
        let table_name = s[7..]
            .chars()
            .into_iter()
            .take_while(|char| char != &'(')
            .collect::<String>();
        let table_right_str = table_name.trim();
        if !check_table_name(table_right_str) {
            println!("provided table name is unacceptable");
            return Err(UnacceptableData);
        }
        let columns_data = &s[(table_right_str.len() + 7 + 2)..];
        let columns = columns_data.split(", ").collect::<Vec<&str>>();
        let mut finished = false;
        let mut table_columns = Vec::new(); //Option<HashMap<String,HashMap<String, usize>>>
        let mut mmmap = None;
        for column_possibly_name in columns {
            if finished {
                return Err(InvalidUsage);
            }
            if column_possibly_name.to_uppercase().ends_with(" INDEXED") {
                if mmmap.is_none() {
                    mmmap = Some(HashMap::new());
                }
                mmmap.as_mut().unwrap().insert(
                    column_possibly_name[..column_possibly_name.len() - 8].to_string(),
                    HashMap::new(),
                );
            }
            if column_possibly_name.to_lowercase().ends_with(");") {
                finished = true;
                table_columns.push(String::from(
                    &column_possibly_name[..column_possibly_name.len() - 2],
                ));
            } else {
                table_columns.push(String::from(column_possibly_name));
            };
        }
        let mut colum = Vec::new();
        (0..table_columns.len()).for_each(|_| colum.push(Vec::new()));
        match db.try_create_table(Table::new(
            String::from(table_right_str),
            table_columns,
            colum,
            mmmap,
        )) {
            Ok(_) => {
                println!("table with name {table_right_str} has been created")
            }
            Err(error_message) => {
                println!("{}", error_message);
                return Err(InvalidUsage);
            }
        }
        // insert table_name ("for first row", "for second row", "for third row");
    } else if let Some(insert_data) = s.to_lowercase().strip_prefix("insert ") {
        let mut data = &s[7..];
        if let Some(_into) = insert_data.strip_prefix("into ") {
            data = &s[12..];
        }
        let table_name = data
            .chars()
            .into_iter()
            .take_while(|char| char != &'(')
            .collect::<String>();
        let table_right_str = table_name.trim();
        if !check_table_name(table_right_str) {
            println!("provided table name is unacceptable");
            return Err(UnacceptableData);
        }
        let columns_data = &data[(table_right_str.len() + 2)..];
        let columns = columns_data.split(", ").collect::<Vec<&str>>();
        let mut finished = false;
        let mut table_columns_data = Vec::new();
        for column_possibly_data in columns {
            if finished
                || !column_possibly_data.starts_with('"')
                || (!column_possibly_data.ends_with('"') && !column_possibly_data.ends_with(';'))
            {
                return Err(InvalidUsage);
            }
            let mut sstr;
            if let Some(_start) = column_possibly_data.strip_suffix(");") {
                finished = true;
                sstr = &column_possibly_data[..column_possibly_data.len() - 2];
            } else {
                sstr = column_possibly_data;
            }
            sstr = &sstr[1..sstr.len() - 1];
            table_columns_data.push(sstr.to_string());
        }
        match db.insert_into_table(table_right_str, table_columns_data) {
            Ok(_) => {
                println!("data into {table_right_str} inserted");
            }
            Err(error_message) => {
                println!("{}", error_message);
                return Err(InvalidUsage);
            }
        }
        /*SELECT FROM cats;
        SELECT FROM cats
          WHERE name = “Murzik”;
        SELECT FROM owners
          FULL_JOIN cats ON owner_id = cat_owner_id;
        SELECT FROM owners
          FULL_JOIN cats ON owner_id = cat_owner_id WHERE name = “Murzik”;
          */
    } else if let Some(select_data) = s.to_lowercase().strip_prefix("select from ") {
        let mut data;
        if !select_data.contains(' ') && select_data.len() > 1 {
            return match db.get_table(&s[12..s.len() - 1].trim()) {
                Ok(table) => {
                    table.print();
                    Ok(())
                }
                Err(error_message) => {
                    println!("{}", error_message);
                    Err(InvalidUsage)
                }
            };
        }
        let table_name = s[12..s.len() - 1]
            .trim()
            .chars()
            .into_iter()
            .take_while(|char| char != &' ')
            .collect::<String>();
        let table_right_str = table_name.trim();
        match db.get_table(table_right_str) {
            Ok(table) => {
                data = table;
            }
            Err(error_message) => {
                println!("{}", error_message);
                return Err(InvalidUsage);
            }
        }
        let mut remainder = &s[12 + table_name.len() + 1..];
        let mut res = data.clone();
        if remainder.to_lowercase().starts_with("full_join ") {
            let table_join = remainder[10..]
                .chars()
                .into_iter()
                .take_while(|char| char != &' ')
                .collect::<String>();
            let join_table = match db.get_table(table_join.as_str()) {
                Ok(table) => table,
                Err(error_message) => {
                    println!("{}", error_message);
                    return Err(InvalidUsage);
                }
            };
            remainder = &remainder[table_join.len() + 10 + 1..];
            let on;
            if remainder.to_lowercase().starts_with("on ") {
                on = remainder[3..]
                    .chars()
                    .into_iter()
                    .take_while(|char| char != &' ')
                    .collect::<String>();
                remainder = &remainder[on.len() + 3 + 1..];
            } else {
                return Err(InvalidUsage);
            }
            let another_on;
            if let Some(_another_on_and_other) = remainder.to_lowercase().strip_prefix("= ") {
                another_on = remainder[2..]
                    .chars()
                    .into_iter()
                    .take_while(|char| char != &' ' && char != &';')
                    .collect::<String>();

                remainder = &remainder[another_on.len() + 2..];
            } else {
                return Err(InvalidUsage);
            }
            if !data.columns.iter().any(|column_name| column_name.eq(&on))
                && !join_table
                    .columns
                    .iter()
                    .any(|column_name| column_name.eq(&another_on))
            {
                println!("tables don't have such columns");
                return Err(UnacceptableData);
            }
            let mut whirlpool = Table::new("whirlpool".to_string(), vec![], vec![], None);
            data.columns
                .iter()
                .for_each(|x| whirlpool.columns.push(x.clone()));
            let interested_2 = join_table
                .columns
                .iter()
                .position(|x| x.eq(&another_on))
                .unwrap();
            join_table
                .columns
                .iter()
                .cloned()
                .filter(|x| x.ne(&another_on))
                .for_each(|x| whirlpool.columns.push(x));
            let interested = data.columns.iter().position(|x| x.eq(&on)).unwrap();
            let mut set_of_joined_from2 = HashSet::new();

            for row_u in 0..data.data.first().unwrap().len() {
                // йдемо по першій таблиці
                let mut row = Vec::new(); // збираємо всі дані рядка в вектор
                for column in 0..data.data.len() {
                    row.push(data.data.get(column).unwrap().get(row_u).unwrap());
                }
                let join_on = row.get(interested).unwrap();
                let mut this_row_from_first_have_pairs = false;
                let len_2 = join_table.data.first().unwrap().len();
                for row_join_i in 0..len_2 {
                    //йдемо по другій таблиці
                    let mut row_join = Vec::new(); // збираємо всі дані рядка в вектор
                    let mut row_s = row.clone();
                    for column_join in 0..join_table.data.len() {
                        row_join.push(
                            join_table
                                .data
                                .get(column_join)
                                .unwrap()
                                .get(row_join_i)
                                .unwrap(),
                        );
                    }
                    if row_join.get(interested_2).unwrap().eq(join_on) {
                        let mut cl = row_join.clone();
                        cl.remove(interested_2);
                        cl.into_iter().for_each(|x| row_s.push(x));
                        set_of_joined_from2.insert(row_join_i);
                        this_row_from_first_have_pairs = true;
                        whirlpool.add_to_table(
                            row_s.iter().map(|&x| x.clone()).collect::<Vec<String>>(),
                        );
                    }
                }
                if !this_row_from_first_have_pairs {
                    let mut mm = row.iter().map(|&x| x.clone()).collect::<Vec<String>>();
                    (0..len_2 - 1)
                        .into_iter()
                        .for_each(|_| mm.push(String::from("")));
                    whirlpool.add_to_table(mm);
                }
            }
            for row_u in 0..join_table.data.first().unwrap().len() {
                // second table
                if set_of_joined_from2.contains(&row_u) {
                    continue;
                }
                let mut row = Vec::new(); // збираємо всі дані рядка в вектор
                for column in 0..join_table.data.len() {
                    row.push(join_table.data.get(column).unwrap().get(row_u).unwrap());
                }
                let mut rrrow = Vec::new();
                (0..interested)
                    .into_iter()
                    .for_each(|_| rrrow.push(String::from("")));
                rrrow.push((*row.get(interested_2).unwrap()).clone());
                (0..data.columns.len() - interested - 1)
                    .into_iter()
                    .for_each(|_| rrrow.push(String::from("")));
                row.remove(interested_2);
                row.iter().for_each(|&x| rrrow.push(x.clone()));
                whirlpool.add_to_table(rrrow);
            }
            res = whirlpool;
        }
        //SELECT FROM owners
        //           FULL_JOIN cats ON owner_id = cat_owner_id WHERE name *= “Murzik”;
        // *where some *= ("1" | id);
        if remainder.starts_with(" ") {
            remainder = &remainder[1..];
        }
        if remainder.to_lowercase().starts_with("where ") {
            let what_where = remainder[6..]
                .chars()
                .into_iter()
                .take_while(|char| char != &' ')
                .collect::<String>();
            remainder = &remainder[what_where.len() + 6 + 1..];
            if !remainder.starts_with("= ") {
                return Err(InvalidUsage);
            }
            remainder = &remainder[2..remainder.len() - 1];
            let mut what_eq;
            if remainder.starts_with('(') && remainder.ends_with(')') {
                what_eq = remainder[1..remainder.len() - 1]
                    .split('|')
                    .collect::<Vec<&str>>();
                what_eq.iter_mut().for_each(|each| *each = each.trim())
            } else {
                what_eq = vec![remainder];
            }
            // if what_where.ends_with('"') && what_where.starts_with('"')
            let mut variants = Vec::new();
            let mut columns = what_eq
                .iter()
                .filter(|&&x| {
                    let a = x.starts_with('"') && x.ends_with('"');
                    if a {
                        variants.push(x.trim_matches('"'))
                    }
                    !a
                })
                .map(|x| *x)
                .collect::<Vec<&str>>();
            columns.push(what_where.as_str());
            let ids: Option<Vec<usize>> = columns
                .iter()
                .map(|&col_name| {
                    res.columns
                        .iter()
                        .position(|string_col_name| string_col_name.eq(col_name))
                })
                .collect();
            let opapo = res
                .columns
                .iter()
                .position(|string_col_name| string_col_name.eq(&what_where));
            if ids.is_none() {
                println!("columns with provided in where ids not in whis world");
                return Err(UnacceptableData);
            }
            match get_eq(&mut res.data, &ids.unwrap()[..], variants, opapo.unwrap()) {
                Ok(_) => (),
                Err(error) => {
                    println!("oh no. cringe: {}", error);
                    return Err(UnacceptableData);
                }
            }
        }
        res.print();
    } else {
        return Err(NotExist);
    }

    Ok(())
}

pub fn get_eq(
    vec: &mut Vec<Vec<String>>,
    columns: &[usize],
    variants: Vec<&str>,
    column_check: usize,
) -> Result<(), &'static str> {
    let mut rows_ids = HashSet::new();
    let mut vecs = Vec::new();
    for (a, vecc) in vec.iter_mut().enumerate() {
        if columns.contains(&a) {
            vecs.push(vecc.iter_mut())
        }
    }
    let mut leeen: Option<usize> = None;
    for vec in vecs.iter() {
        if leeen.is_none() {
            leeen = Some(vec.len());
            continue;
        }
        if leeen.unwrap() != vec.len() {
            return Err("very bad error");
        }
    }
    for i in 0..leeen.unwrap() {
        let mut elem;
        elem = None;
        let mut ii = 0;
        for vec in vecs.iter_mut() {
            let n = vec.next();
            if ii == column_check && n.is_some() && !variants.contains(&&***n.as_ref().unwrap()) {
                rows_ids.insert(i);
            }
            match elem.as_ref() {
                None => {
                    elem = Some(n.unwrap().clone());
                    ii += 1;
                    continue;
                }
                Some(el) => {
                    if el.ne(&n.as_ref().unwrap().as_str()) {
                        rows_ids.insert(i);
                    }
                    ii += 1;
                }
            }
        }
    }
    let mut lollll = rows_ids.into_iter().collect::<Vec<usize>>();
    lollll.sort();
    lollll.reverse();
    for vector in vec {
        for i in lollll.iter() {
            vector.remove(*i);
        }
    }
    Ok(())
}
