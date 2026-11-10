pub enum Error { InsufficientFunds, Overflow }
pub struct Wallet { pub balance: u64 }
impl Wallet {
    pub fn deposit(&mut self, amt: u64) -> Result<(), Error> {
        match self.balance.checked_add(amt) {
            Some(b) => { self.balance = b; Ok(()) }
            None => Err(Error::Overflow),
        }
    }
    pub fn withdraw(&mut self, amt: u64) -> Result<(), Error> {
        if amt > self.balance { return Err(Error::InsufficientFunds); }
        self.balance -= amt;
        Ok(())
    }
}
pub fn transfer(src: &mut Wallet, dst: &mut Wallet, amt: u64) -> Result<(), Error> {
    if src.balance < amt { return Err(Error::InsufficientFunds); }
    let nb = match dst.balance.checked_add(amt) { Some(b) => b, None => return Err(Error::Overflow) };
    src.balance -= amt;
    dst.balance = nb;
    Ok(())
}
