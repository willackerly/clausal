// A parameter named like a module of the crate. The generated Lean contains `input.Input.get input`, which Lean
// elaborates as a field access on the parameter `input`.
pub mod input {
    pub struct Input {
        pub value: u32,
    }
    impl Input {
        pub fn get(&self) -> u32 {
            self.value
        }
    }
}
pub mod shadow {
    use crate::input;
    pub fn param_like_module(input: input::Input) -> u32 {
        input.get()
    }
}
