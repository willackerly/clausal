//! fninv: syntactic inventory of every `fn` with a body in a set of Rust files.
//! Usage: fninv <crate-root> <file.rs>...   (prints one JSON array on stdout)
//! Independent of Charon: this is the census denominator.
use proc_macro2::Span;
use quote::ToTokens;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use syn::spanned::Spanned;
use syn::visit::{self, Visit};

#[derive(Default, Clone)]
struct Feat {
    c: BTreeMap<&'static str, u64>,
    macros: BTreeMap<String, u64>,
    methods: BTreeMap<String, u64>,
}
impl Feat {
    fn inc(&mut self, k: &'static str) {
        *self.c.entry(k).or_insert(0) += 1;
    }
}

struct Ctx {
    file: String,
    out: Vec<Value>,
    // stack of enclosing item descriptions
    path: Vec<String>,
    cfgs: Vec<Vec<String>>,
    test_depth: u32,
    fn_stack: Vec<FnFrame>,
}
struct FnFrame {
    feat: Feat,
    loop_depth: u32,
    closure_depth: u32,
}

fn line(s: Span) -> (usize, usize) {
    (s.start().line, s.end().line)
}
fn attr_strings(attrs: &[syn::Attribute]) -> (Vec<String>, bool, bool) {
    let mut cfgs = vec![];
    let mut is_test = false;
    let mut cfg_test = false;
    for a in attrs {
        let p = a.path().to_token_stream().to_string().replace(' ', "");
        if p == "cfg" {
            let s = a.meta.to_token_stream().to_string();
            if s.contains("test") && !s.contains("not (test") && !s.contains("not(test") {
                cfg_test = true;
            }
            cfgs.push(s);
        }
        if p == "test" || p.ends_with("::test") || p == "bench" {
            is_test = true;
        }
    }
    (cfgs, is_test, cfg_test)
}
fn ty_has(t: &dyn ToTokens, needle: &str) -> bool {
    t.to_token_stream().to_string().split(|c: char| !c.is_alphanumeric() && c != '_').any(|w| w == needle)
}

impl Ctx {
    fn f(&mut self) -> Option<&mut FnFrame> {
        self.fn_stack.last_mut()
    }
    fn enter_fn(
        &mut self,
        kind: &str,
        name: String,
        attrs: &[syn::Attribute],
        sig: &syn::Signature,
        whole: Span,
        block: &syn::Block,
        vis_pub: bool,
    ) {
        let (cfgs, is_test, cfg_test) = attr_strings(attrs);
        let mut feat = Feat::default();
        if sig.unsafety.is_some() { feat.inc("unsafe_fn"); }
        if sig.asyncness.is_some() { feat.inc("async_fn"); }
        if sig.constness.is_some() { feat.inc("const_fn"); }
        let ntp = sig.generics.type_params().count() as u64;
        if ntp > 0 { feat.c.insert("type_params", ntp); }
        let nlt = sig.generics.lifetimes().count() as u64;
        if nlt > 0 { feat.c.insert("lifetime_params", nlt); }
        if sig.generics.const_params().count() > 0 { feat.inc("const_params"); }
        let bounded = sig.generics.type_params().any(|t| !t.bounds.is_empty()) || sig.generics.where_clause.is_some();
        if bounded { feat.inc("trait_bounds"); }
        let sigs = sig.to_token_stream().to_string();
        if sigs.contains("impl ") { feat.inc("sig_impl_trait"); }
        if sigs.contains("dyn ") { feat.inc("sig_dyn"); }
        if sigs.contains("& mut") || sigs.contains("&mut") { feat.inc("sig_mut_ref"); }
        if sigs.contains("for <") { feat.inc("sig_hrtb"); }
        for w in ["f32", "f64", "String", "str", "Box", "Rc", "Arc", "RefCell", "Cell", "HashMap", "HashSet", "BTreeMap", "BTreeSet", "Vec", "Formatter", "Fn", "FnMut", "FnOnce", "Iterator", "IntoIterator", "Self"] {
            if ty_has(sig, w) { feat.c.insert(match w {
                "f32" | "f64" => "sig_float", "String" | "str" => "sig_string", "Box" => "sig_box",
                "Rc" | "Arc" => "sig_rc", "RefCell" | "Cell" => "sig_cell",
                "HashMap" | "HashSet" | "BTreeMap" | "BTreeSet" => "sig_map", "Vec" => "sig_vec",
                "Formatter" => "sig_formatter", "Fn" | "FnMut" | "FnOnce" => "sig_fn_trait",
                "Iterator" | "IntoIterator" => "sig_iterator", _ => "sig_self" }, 1); }
        }
        let (l0, l1) = line(whole);
        let (s0, _) = line(sig.span());
        let (b0, b1) = line(block.span());
        self.fn_stack.push(FnFrame { feat, loop_depth: 0, closure_depth: 0 });
        let mut all_cfgs: Vec<String> = self.cfgs.iter().flatten().cloned().collect();
        all_cfgs.extend(cfgs.clone());
        let rec = json!({
            "file": self.file, "name": name, "kind": kind,
            "path": self.path.join("::"),
            "line_start": l0, "sig_line": s0, "body_start": b0, "line_end": l1.max(b1),
            "is_test": is_test || cfg_test || self.test_depth > 0,
            "cfgs": all_cfgs, "public": vis_pub,
            "nested_in_fn": self.fn_stack.len() > 1,
            "n_stmts": block.stmts.len(),
        });
        self.path.push(name_seg(&rec));
        visit::visit_block(self, block);
        self.path.pop();
        let fr = self.fn_stack.pop().unwrap();
        let mut rec = rec;
        rec["feat"] = json!(fr.feat.c);
        rec["macros"] = json!(fr.feat.macros);
        rec["methods"] = json!(fr.feat.methods);
        self.out.push(rec);
    }
}
fn name_seg(v: &Value) -> String {
    v["name"].as_str().unwrap().to_string()
}

impl<'ast> Visit<'ast> for Ctx {
    fn visit_item_mod(&mut self, m: &'ast syn::ItemMod) {
        let (cfgs, _t, cfg_test) = attr_strings(&m.attrs);
        self.path.push(m.ident.to_string());
        self.cfgs.push(cfgs);
        if cfg_test { self.test_depth += 1; }
        visit::visit_item_mod(self, m);
        if cfg_test { self.test_depth -= 1; }
        self.cfgs.pop();
        self.path.pop();
    }
    fn visit_item_impl(&mut self, i: &'ast syn::ItemImpl) {
        let (cfgs, _t, cfg_test) = attr_strings(&i.attrs);
        let ty = i.self_ty.to_token_stream().to_string().replace(' ', "");
        let seg = match &i.trait_ {
            Some((_, p, _)) => format!("{{impl {} for {}}}", p.to_token_stream().to_string().replace(' ', ""), ty),
            None => format!("{{impl {}}}", ty),
        };
        self.path.push(seg);
        self.cfgs.push(cfgs);
        if cfg_test { self.test_depth += 1; }
        visit::visit_item_impl(self, i);
        if cfg_test { self.test_depth -= 1; }
        self.cfgs.pop();
        self.path.pop();
    }
    fn visit_item_trait(&mut self, t: &'ast syn::ItemTrait) {
        let (cfgs, _t, _) = attr_strings(&t.attrs);
        self.path.push(format!("{{trait {}}}", t.ident));
        self.cfgs.push(cfgs);
        visit::visit_item_trait(self, t);
        self.cfgs.pop();
        self.path.pop();
    }
    fn visit_item_fn(&mut self, f: &'ast syn::ItemFn) {
        let p = matches!(f.vis, syn::Visibility::Public(_));
        self.enter_fn("free", f.sig.ident.to_string(), &f.attrs, &f.sig, f.span(), &f.block, p);
    }
    fn visit_impl_item_fn(&mut self, f: &'ast syn::ImplItemFn) {
        let p = matches!(f.vis, syn::Visibility::Public(_));
        let kind = if self.path.last().map(|s| s.contains(" for ")).unwrap_or(false) { "trait_impl_method" } else { "inherent_method" };
        self.enter_fn(kind, f.sig.ident.to_string(), &f.attrs, &f.sig, f.span(), &f.block, p);
    }
    fn visit_trait_item_fn(&mut self, f: &'ast syn::TraitItemFn) {
        if let Some(b) = &f.default {
            self.enter_fn("trait_default_method", f.sig.ident.to_string(), &f.attrs, &f.sig, f.span(), b, true);
        }
    }
    fn visit_expr_for_loop(&mut self, e: &'ast syn::ExprForLoop) {
        let is_range = matches!(&*e.expr, syn::Expr::Range(_))
            || matches!(&*e.expr, syn::Expr::Paren(p) if matches!(&*p.expr, syn::Expr::Range(_)));
        if let Some(f) = self.f() {
            f.feat.inc("for_loop");
            if is_range { f.feat.inc("for_range"); } else { f.feat.inc("for_iter"); }
            if f.loop_depth > 0 { f.feat.inc("nested_loop"); }
            f.loop_depth += 1;
        }
        visit::visit_expr_for_loop(self, e);
        if let Some(f) = self.f() { f.loop_depth -= 1; }
    }
    fn visit_expr_while(&mut self, e: &'ast syn::ExprWhile) {
        let is_let = e.cond.to_token_stream().to_string().starts_with("let ");
        if let Some(f) = self.f() {
            f.feat.inc("while_loop");
            if is_let { f.feat.inc("while_let"); }
            if f.loop_depth > 0 { f.feat.inc("nested_loop"); }
            f.loop_depth += 1;
        }
        visit::visit_expr_while(self, e);
        if let Some(f) = self.f() { f.loop_depth -= 1; }
    }
    fn visit_expr_loop(&mut self, e: &'ast syn::ExprLoop) {
        if let Some(f) = self.f() {
            f.feat.inc("loop_loop");
            if f.loop_depth > 0 { f.feat.inc("nested_loop"); }
            f.loop_depth += 1;
        }
        visit::visit_expr_loop(self, e);
        if let Some(f) = self.f() { f.loop_depth -= 1; }
    }
    fn visit_expr_return(&mut self, e: &'ast syn::ExprReturn) {
        if let Some(f) = self.f() {
            if f.closure_depth == 0 {
                f.feat.inc("return");
                if f.loop_depth > 0 { f.feat.inc("return_in_loop"); }
                if f.loop_depth > 1 { f.feat.inc("return_in_nested_loop"); }
            }
        }
        visit::visit_expr_return(self, e);
    }
    fn visit_expr_try(&mut self, e: &'ast syn::ExprTry) {
        if let Some(f) = self.f() {
            f.feat.inc("try_op");
            if f.loop_depth > 0 && f.closure_depth == 0 { f.feat.inc("try_in_loop"); }
        }
        visit::visit_expr_try(self, e);
    }
    fn visit_expr_break(&mut self, e: &'ast syn::ExprBreak) {
        if let Some(f) = self.f() {
            f.feat.inc("break");
            if e.label.is_some() { f.feat.inc("labeled_break"); }
            if e.expr.is_some() { f.feat.inc("break_value"); }
        }
        visit::visit_expr_break(self, e);
    }
    fn visit_expr_continue(&mut self, e: &'ast syn::ExprContinue) {
        if let Some(f) = self.f() {
            f.feat.inc("continue");
            if e.label.is_some() { f.feat.inc("labeled_continue"); }
        }
        visit::visit_expr_continue(self, e);
    }
    fn visit_expr_closure(&mut self, e: &'ast syn::ExprClosure) {
        if let Some(f) = self.f() { f.feat.inc("closure"); f.closure_depth += 1; }
        visit::visit_expr_closure(self, e);
        if let Some(f) = self.f() { f.closure_depth -= 1; }
    }
    fn visit_expr_unsafe(&mut self, e: &'ast syn::ExprUnsafe) {
        if let Some(f) = self.f() { f.feat.inc("unsafe_block"); }
        visit::visit_expr_unsafe(self, e);
    }
    fn visit_expr_async(&mut self, e: &'ast syn::ExprAsync) {
        if let Some(f) = self.f() { f.feat.inc("async_block"); }
        visit::visit_expr_async(self, e);
    }
    fn visit_expr_await(&mut self, e: &'ast syn::ExprAwait) {
        if let Some(f) = self.f() { f.feat.inc("await"); }
        visit::visit_expr_await(self, e);
    }
    fn visit_expr_match(&mut self, e: &'ast syn::ExprMatch) {
        if let Some(f) = self.f() { f.feat.inc("match"); }
        visit::visit_expr_match(self, e);
    }
    fn visit_expr_index(&mut self, e: &'ast syn::ExprIndex) {
        let r = matches!(&*e.index, syn::Expr::Range(_));
        if let Some(f) = self.f() { f.feat.inc("index"); if r { f.feat.inc("index_range"); } }
        visit::visit_expr_index(self, e);
    }
    fn visit_expr_cast(&mut self, e: &'ast syn::ExprCast) {
        let t = e.ty.to_token_stream().to_string();
        if let Some(f) = self.f() {
            f.feat.inc("as_cast");
            if t.contains('*') { f.feat.inc("ptr_cast"); }
            if t == "f32" || t == "f64" { f.feat.inc("float"); }
        }
        visit::visit_expr_cast(self, e);
    }
    fn visit_expr_range(&mut self, e: &'ast syn::ExprRange) {
        if let Some(f) = self.f() { f.feat.inc("range_expr"); }
        visit::visit_expr_range(self, e);
    }
    fn visit_lit_float(&mut self, l: &'ast syn::LitFloat) {
        if let Some(f) = self.f() { f.feat.inc("float"); }
        visit::visit_lit_float(self, l);
    }
    fn visit_lit_str(&mut self, l: &'ast syn::LitStr) {
        if let Some(f) = self.f() { f.feat.inc("str_literal"); }
        visit::visit_lit_str(self, l);
    }
    fn visit_type_path(&mut self, t: &'ast syn::TypePath) {
        if let Some(seg) = t.path.segments.last() {
            let s = seg.ident.to_string();
            if let Some(f) = self.f() {
                match s.as_str() {
                    "f32" | "f64" => f.feat.inc("float"),
                    "RefCell" | "Cell" | "UnsafeCell" | "OnceCell" | "Mutex" | "RwLock" | "AtomicUsize" | "AtomicBool" | "AtomicU64" => f.feat.inc("interior_mut"),
                    _ => {}
                }
            }
        }
        visit::visit_type_path(self, t);
    }
    fn visit_type_trait_object(&mut self, t: &'ast syn::TypeTraitObject) {
        if let Some(f) = self.f() { f.feat.inc("dyn_in_body"); }
        visit::visit_type_trait_object(self, t);
    }
    fn visit_expr_method_call(&mut self, e: &'ast syn::ExprMethodCall) {
        let n = e.method.to_string();
        if let Some(f) = self.f() {
            f.feat.inc("method_call");
            *f.feat.methods.entry(n).or_insert(0) += 1;
        }
        visit::visit_expr_method_call(self, e);
    }
    fn visit_macro(&mut self, m: &'ast syn::Macro) {
        let n = m.path.segments.last().map(|s| s.ident.to_string()).unwrap_or_default();
        if let Some(f) = self.f() {
            f.feat.inc("macro_call");
            *f.feat.macros.entry(n.clone()).or_insert(0) += 1;
        }
        // Look inside the common expression-like macros so that closures/loops/method calls in
        // their arguments are counted (best effort: parse the arguments as comma-separated exprs).
        if let Ok(args) = m.parse_body_with(syn::punctuated::Punctuated::<syn::Expr, syn::Token![,]>::parse_terminated) {
            for a in args.iter() { self.visit_expr(a); }
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let root = std::path::PathBuf::from(&args[1]);
    let mut all = vec![];
    let mut errors = vec![];
    for f in &args[2..] {
        let p = root.join(f);
        let src = match std::fs::read_to_string(&p) { Ok(s) => s, Err(e) => { errors.push(json!({"file": f, "error": e.to_string()})); continue; } };
        match syn::parse_file(&src) {
            Ok(file) => {
                let mut c = Ctx { file: f.clone(), out: vec![], path: vec![], cfgs: vec![], test_depth: 0, fn_stack: vec![] };
                let (cfgs, _, cfg_test) = attr_strings(&file.attrs);
                c.cfgs.push(cfgs);
                if cfg_test { c.test_depth += 1; }
                c.visit_file(&file);
                all.extend(c.out);
            }
            Err(e) => errors.push(json!({"file": f, "error": e.to_string()})),
        }
    }
    println!("{}", serde_json::to_string(&json!({"functions": all, "parse_errors": errors})).unwrap());
}
