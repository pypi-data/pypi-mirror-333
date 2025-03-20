use std::env;
use std::path::PathBuf;

fn main() {

    // for debug only
    env::set_var("LIBRARY_PATH", "/home/erik.vonreis/fakeroot/lib");
    env::set_var("LD_LIBRARY_PATH", "/home/erik.vonreis/fakeroot/lib");
    let inc_dir = "/home/erik.vonreis/fakeroot/include";
    env::set_var("C_INCLUDE_PATH", inc_dir);
    env::set_var("CPLUS_INCLUDE_PATH", inc_dir);

    println!("cargo:rustc-link-search=/home/erik.vonreis/fakeroot/lib");
    println!("cargo:rustc-link-lib=gds-sigp");
    println!("cargo:rustc-link-lib=cds");
    // println!("cwd={}", env::current_dir().expect("No working directory").to_str().expect("cwd not a string"));
    let bindings = bindgen::Builder::default()
        //.clang_arg("-I/home/erik.vonreis/fakeroot/include")
        //.clang_arg("-L/home/erik.vonreis/fakeroot/lib")
        .header("wrapper.h")
        // .parse_callbacks(Box::new(bindgen::CargoCallbacks{
        //
        // }))
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out_path.join("bindings.rs")).expect("Couldn't write bindings");

    // cxx_build::bridge("src/data_source/nds2.rs").file("src/data_source/nds2.cpp").flag_if_supported("-std=c++17").compile("nds2bridge");
    // println!("cargo:rerun-if-changed=src/data_source/nds2.rs");
    // println!("cargo:rerun-if-changed=src/data_source/nds2.cpp");
    // println!("cargo:rerun-if-changed=include/nds2.h");
    // println!("cargo:rustc-link-lib=ndsclient");
    // println!("cargo:rustc-link-lib=ndscxx");
}