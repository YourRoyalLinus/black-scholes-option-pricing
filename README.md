# Black-Scholes Option Pricing Calculator
*Requires Python version 3.5 or later*  

The Black-Scholes option pricing calculator is a command line tool used to calculate the price and corresponding Greek values of a financial derivative, provided a few inputs.   If these inputs are not provided as arguments when first executing the program, you will be prompted for them.  

### Inputs
- ##### Required
   * A CSV file with the following two fields:
      * Date
      * Close
   * Target strike price
   * The expiration date of the derivative in YYYY-MM-DD format. 

  Arbitrarily, at least 100 days' worth of historical data should be provided for the model to be assumed accurate.  
  A CSV downloaded from [Yahoo Finance](https://finance.yahoo.com/) under the '[Historical Data](https://finance.yahoo.com/quote/MASI/history?p=MASI)' tab can be used without further change

 - ##### Optional
    * Option Type - 'c' for Call and 'p' for Put
      * A 'c' or 'p' can be postfixed to the strike price input - EG: s 100c OR s 100p. However, the option type flag will take precedence if both are included
      * Defaults to Call if no option type is provided
   * Risk-Free Rate 
     * See [Limitations](#Limitations) for information about defaulted Risk-Free Rates
   * Name or Ticker Symbol - Can be any way you want to identify the information you're calculating 
### Assumptions
* There are an average of 253 trading days per year
* Rounding is done only before display with a precision of 4
* Risk free rate is defaulted to the yield of a [3-month Treasury Bill](https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/textview.aspx?data=yield) as of 1/14/2022 (.13%) 
### Limitations
* The model is only accurate for European option contracts, due to the nature of how time to expiration is calculated
* The model does not take into account dividend yield. 
  * Dividend paying stocks can be modeled, however its pricing and corresponding Greeks should not be considered accurate

### Examples
* Historical Data - [Masimo Corporation (MASI)](https://finance.yahoo.com/quote/MASI/history?p=MASI)  
  
  `py main.py -f PATH\TO\CSV\MASI.csv -s 220c -x 2022-02-18`
  ```
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Company              | Underlying Price |  Target Strike  | Risk Free Rate  | Expiration Date | Expected Call Price |
  |                N/A                | $    217.91      | $    220.0      |     0.0013    % |   2022-02-18    | $      5.5349       |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Greeks               |      Delta      |      Gamma       |      Theta      |      Vega       |         Rho         |
  |               Call                |     0.4644      |      0.0244      |     -0.1841     |     0.2284      |       0.0666        |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ```
  
  `py main.py`
  
  Please enter a historical data file to build the  Black-Scholes model (Rerun with flag -h or --help to for more information): `PATH\TO\CSV\MASI.csv`  
  Please enter a targeted strike price (Rerun with flag -h or --help to for more information): `220`  
  Please enter an expiration date of the contract in <YYYY-MM-DD> format (Rerun with flag -h or --help to for more information): `2022-02-18` 
  ```
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Company              | Underlying Price |  Target Strike  | Risk Free Rate  | Expiration Date | Expected Call Price |
  |                N/A                | $    217.91      | $    220.0      |     0.0013    % |   2022-02-18    | $      5.534        |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Greeks               |      Delta      |      Gamma       |      Theta      |      Vega       |         Rho         |
  |               Call                |     0.4644      |      0.0244      |     -0.1841     |     0.2284      |       0.0665        |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ```
  
  `py main.py -f PATH\TO\CSV\MASI.csv -s 215p -x 2022-02-18 --name MASI`
  ```
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Company              | Underlying Price |  Target Strike  | Risk Free Rate  | Expiration Date | Expected Put Price |
  |               MASI                | $    217.91      | $    215.0      |     0.0013    % |   2022-02-18    | $      5.0827       |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  |              Greeks               |      Delta      |      Gamma       |      Theta      |      Vega       |         Rho         |
  |                Put                |     -0.4134     |      0.024       |     -0.1795     |     0.2238      |       -0.0662       |
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  ```

---
## Program Flags
* -s, --strike_price {ARG}
* -f, --file {ARG}
* -x, --expiration_date {ARG}
* -o, --option_type {ARG}
* -r, --risk_free {ARG}
* -n, --name {ARG}     
* -h, --help
---
## Future Improvements
* Add support for modeling of American option contracts
* Add support for Dividend yielding securities
* Improve how calculations are displayed
