######################################################################################################################
def print_banner():
    banner = """
                ╔══════════════════════════════════════════════════════════╗
                ║  🚀 ORCA INPUT GENERATOR – POWERED BY SCIENCE & CHAOS ☢️║
                ╠══════════════════════════════════════════════════════════╣
                ║  Author: Ananda Thongyu 🧪💀                            ║
                ║  Version: 3.21 (Because perfection is an illusion)       ║
                ║  Year: 2025                                              ║
                ╠══════════════════════════════════════════════════════════╣
                🛠️ This script is BUILT DIFFERENT.                     
                🚨 It doesn’t just generate ORCA inputs –              
                    it engineers **computational perfection**.           

                💥 Features that SLAP:                                 
                ✅ TD-DFT? Hell yeah.                                  
                ✅ CPCMC(WATER)? You know it.                         
                ✅ NEB-TS, NEB-CI, FAST-NEB-TS, LOOSE, TIGHT? ALL IN.  
                ✅ ESD(PHOSP) & ISC? Advanced level unlocked.   
                                                          
                ⚡ HOW TO USE:                                         
                - Run the script.                                      
                - Answer the questions.                                 
                - Get a BANGER of an ORCA input file.                   
                - Hit submit and flex on your colleagues.               
                                                        
                🔥 REMEMBER:                                            
                - SCF will fail when you least expect it.               
                - DFT is a lie, but a useful one.                       
                                                            

             🏴‍☠️ May your optimizations converge faster than your energies. 🔥 LET'S GOOOOOOO 🔥                 END
         ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

print_banner()

# Function to ask for user input with default values
def get_input(prompt, default=None):
    """
    Prompts the user for input and returns the input or a default value.

    Args:
        prompt (str): The prompt shown to the user.
        default (str): The default value if the user provides no input.

    Returns:
        str: The user input or the default value.
    """
    user_input = input(f"{prompt} [{default}]: ")
    return user_input if user_input else default

# Function to ask for user input with a numeric selection
def get_selection(prompt, options):
    """
    Prompts the user to select an option from a list of choices.

    Args:
        prompt (str): The prompt message shown to the user.
        options (list): List of selectable options.

    Returns:
        str: The selected option.
    """
    print(f"{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input(f"Select an option (1-{len(options)}): "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Invalid selection. Please choose a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")

# Function to ask for numeric input with validation
def get_numeric_input(prompt, default=None, input_type=int):
    """
    Prompts the user for a numeric input and ensures valid input.

    Args:
        prompt (str): The prompt shown to the user.
        default (int or float): The default value if no input is provided.
        input_type (type): The type of the numeric input, either int or float.

    Returns:
        int or float: The valid numeric input or default.
    """
    while True:
        user_input = input(f"{prompt} [{default}]: ")
        if not user_input:
            return default
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Please enter a valid {input_type.__name__}.")

# Function to get functional and basis set selections
def get_functional_basis():
    """
    Asks the user to select a functional and a basis set.

    Returns:
        tuple: Selected functional and basis set.
    """
    functionals = [
        "B3LYP", "PBE", "PBE0", "RHF", "CAM-B3LYP", "M06", "B97-D3",
        "HSE06", "M06-2X"
    ]
    basis_sets = [
        "aug-cc-pVDZ", "aug-cc-pVTZ", "aug-cc-pVQZ", "def2-SVP", "def2-TZVP", "def2-QZVP",
        "def2-SVPD", "def2-TZVPP", "def2-QZVPP", "6-31G(d,p)", "cc-pVDZ", "cc-pVTZ", "OLD-SVP"
    ]
    functional = get_selection("Select the functional", functionals)
    basis_set = get_selection("Select the basis set", basis_sets)

    return functional, basis_set

# Function to get method selection
def get_method():
    """
    Asks the user to select the calculation method.

    Returns:
        str: Selected method.
    """
    methods = ["opt", "sp", "neb", "ci-opt", "ts-opt", "ESD(PHOSP)", "ESD(ISC)"]
    method = get_selection("Select the method", methods)

    if method == "ESD(PHOSP)":
        return "PHOSP"

    if method == "ESD(ISC)":
        return "ISC"
    
    if method == "opt":
        opt_methods = ["OPT", "OPT FREQ", "OPT NUMFREQ"]
        opt_choice = get_selection("Select opt function", opt_methods)
        return opt_choice
    
    if method == "neb":
        # Ask user for NEB sub-methods
        neb_methods = ["NEB", "NEB-CI", "NEB-TS", "FAST-NEB-TS", "LOOSE-NEB-TS", "TIGHT-NEB-TS"]
        neb_choice = get_selection("Select NEB method", neb_methods)
        return neb_choice  # Return specific NEB method
    
    return method

# Function to ask whether to include CPCMC(WATER)
def include_cpcmc():
    """
    Asks the user whether to include CPCMC(WATER) in the calculation input.

    Returns:
        bool: True if CPCMC(WATER) is to be included, False otherwise.
    """
    return get_selection("Include CPCMC(WATER)?", ["YES", "NO"]) == "YES"

def include_tddft():
    """
    Asks the user whether to include TD-DFT in the calculation input.

    Returns:
        bool: True if TD-DFT is to be included, False otherwise.
    """
    return get_selection("Include TD-DFT?", ["YES", "NO"]) == "YES"

def generate_dft_block(method, nroots, iroot, iroot_mult, maxiter, functional, basis_set, coord_file, include_cpcmc, include_tddft, charge, multi):
    """
    Generates the DFT block for the input file.

    Args:
        nroots (int): Number of TDDFT roots.
        iroot (int): The root to optimize.
        iroot_mult (str): The spin multiplicity (Singlet or Triplet).

    Returns:
        str: TDDFT block as a string.
    """
    cpcmc_line = "CPCMC(WATER)" if include_cpcmc else ""
    tddft_block = f"""
%TDDFT
    NRoots {nroots}
    IRoot {iroot}
    IRootMult {iroot_mult}
    MaxIter {maxiter}
    Maxcore 16000
end
""" if include_tddft else ""

    return f""" 
!{functional}  {method}  {basis_set} TIGHTSCF {cpcmc_line}

{tddft_block}

%maxcore 16000
* xyzfile {charge} {multi} {coord_file}
"""

def generate_neb_block(method, nroots, iroot, iroot_mult, maxiter, functional, basis_set, coord_file, include_cpcmc, include_tddft, product_file, NIm, Plevel, charge, multi):
    """
    Generates the NEB-TS block for the input file.

    Args:
        coord_file (str): The XYZ coordinate file.
        include_cpcmc (bool): Whether to include CPCMC(WATER).
        include_tddft (bool): Whether to include TDDFT.
        product_file (str): The XYZ coordinate file for the product.
        NIm (int): Number of images.
        Plevel (int): Print level.
        charge (int): Molecular charge.
        multi (int): Spin multiplicity.

    Returns:
        str: NEB-TS block as a string.
    """
    cpcmc_line = "CPCMC(WATER)" if include_cpcmc else ""
    tddft_block = f"""
%TDDFT
    NRoots {nroots}
    IRoot {iroot}
    IRootMult {iroot_mult}
    MaxIter {maxiter}
    Maxcore 16000
end
""" if include_tddft else ""

    return f""" 
!{functional} FREQ {method} {basis_set} TIGHTSCF {cpcmc_line}

{tddft_block}

%NEB
    Product "{product_file}"    # Product structure. Input is mandatory.
    NImages {NIm}               # Default 8. Number of images without fixed endpoints.
    PrintLevel {Plevel}         # Default 1. Normal printout. Use 0 for no printout, higher values for more detail.
END

* xyzfile {charge} {multi} {coord_file}
"""


# Function to generate input blocks for specific methods
def generate_phosphorescence_blocks(nroots, iroot_start, g_hessian, t_hessian, dele, functional, basis_set, coord_file, include_cpcmc, charge, multi):
    """
    Generates blocks for phosphorescence calculations in the ORCA input file.

    Args:
        nroots (int): Number of TDDFT roots.
        iroot_start (int): Starting root for optimization.
        g_hessian (str): Path to G Hessian file.
        t_hessian (str): Path to T Hessian file.
        dele (float): DELE value for ESD block.
        functional (str): Functional to use.
        basis_set (str): Basis set to use.
        coord_file (str): Coordinate file name.
        include_cpcmc (bool): Whether to include CPCMC(WATER).

    Returns:
        str: Combined phosphorescence blocks as a string.
    """
    cpcmc_line = " CPCMC(WATER)" if include_cpcmc else ""
    blocks = []
    for i in range(nroots):
        blocks.append(f"""
!{functional} {basis_set} TIGHTSCF ESD(PHOSP) RI-SOMF(1X) {cpcmc_line}

%TDDFT
  NROOTS  {nroots}
  DOSOC   TRUE
  TDA     FALSE
  IROOT   {iroot_start + i}
  TRIPLETS TRUE
END

%ESD
    GSHESSIAN "{g_hessian}"
    TSHESSIAN "{t_hessian}"
    DOHT      TRUE
    DELE      {dele}
END

%maxcore 16000
* xyzfile {charge} {multi} {coord_file}
""")

    return "$NEW_JOB".join(blocks)

def generate_isc_blocks(nroots, sroot, troot, trootssl, isc_ishess, isc_fshess, usej, temp, dele, functional, basis_set, coord_file, include_cpcmc, charge, multi):
    """
    Generates blocks for ESD(ISC) calculations in the ORCA input file.

    Args:
        nroots (int): Number of TDDFT roots.
        sroot (int): SROOT parameter.
        troot (int): TROOT parameter.
        trootssl (int): TROOTSSL parameter.
        isc_ishess (str): Path to ISCISHESS file.
        isc_fshess (str): Path to ISCFSHESS file.
        usej (bool): Whether to use J in ESD.
        temp (float): Temperature for ESD calculations.
        dele (float): DELE value.
        functional (str): Functional to use.
        basis_set (str): Basis set to use.
        coord_file (str): Coordinate file name.
        include_cpcmc (bool): Whether to include CPCMC(WATER).

    Returns:
        str: Combined ISC blocks as a string.
    """
    cpcmc_line = " CPCMC(WATER)" if include_cpcmc else ""
    return f"""
!{functional} {basis_set} TIGHTSCF ESD(ISC) {cpcmc_line} AUTOSTART

%TDDFT
  NROOTS  {nroots}
  SROOT   {sroot}
  TROOT   {troot}
  TROOTSSL {trootssl}
  DOSOC   TRUE
END

%ESD
    ISCISHESS       "{isc_ishess}"
    ISCFSHESS       "{isc_fshess}"
    USEJ            {"TRUE" if usej else "FALSE"}
    DOHT            TRUE
    TEMP            {temp}
    DELE            {dele}
END

* xyzfile {charge} {multi} {coord_file}
"""

# Main program
def main():
    # Collect processor information
    nprocs = get_input("Specify number of processors", default="8")

    # Collect functional and basis set using the expanded selection method
    functional, basis_set = get_functional_basis()

    # Ask whether to include CPCMC(WATER)
    include_cpcmc_flag = include_cpcmc()
    include_tddft_flag = include_tddft()

    # Collect the method
    method = get_method()

    # Create basic input string
    input_file = f"""%pal nprocs {nprocs}
end

"""

    # Get other essential input parameters
    charge = get_input("Charge of the system", default="0")
    multi = get_input("Multiplicity of the system", default="1")
    coord_file = get_input("Coordinate file (e.g., orca_coord.xyz)", default="orca_coord.xyz")

    # Check if phosphorescence calculations are required based on method
    if method == "PHOSP":
        nroots = get_numeric_input("Number of TDDFT roots", default=3)
        iroot_start = get_numeric_input("Starting IRoot", default=1)
        g_hessian = get_input("Specify GSHESSIAN file name", default="vert_t1_cos_g.hess")
        t_hessian = get_input("Specify TSHESSIAN file name", default="vert_t1_cos_t.hess")
        dele = get_numeric_input("Specify DELE value for ESD block", default=15741, input_type=float)
        input_file += generate_phosphorescence_blocks(nroots, iroot_start, g_hessian, t_hessian, dele, functional, basis_set, coord_file, include_cpcmc_flag, charge, multi)

    elif method == "ISC":
        nroots = get_numeric_input("Number of TDDFT roots", default=3)
        sroot = get_numeric_input("Specify SROOT", default=1)
        troot = get_numeric_input("Specify TROOT", default=1)
        trootssl = get_numeric_input("Specify TROOTSSL", default=0)
        isc_ishess = get_input("Specify ISCISHESS file name", default="HESS_S1_SOC_COS78.hess")
        isc_fshess = get_input("Specify ISCFSHESS file name", default="HESS_T1_SOC_COS78.hess")
        usej = get_selection("Use J in ESD?", ["TRUE", "FALSE"]) == "TRUE"
        temp = get_numeric_input("Specify temperature (TEMP)", default=298.0, input_type=float)
        dele = get_numeric_input("Specify DELE value", default=1298.4, input_type=float)

        # Add a second ISC block with TROOTSSL set to -1
        input_file += generate_isc_blocks(nroots, sroot, troot, trootssl, isc_ishess, isc_fshess, usej, temp, dele, functional, basis_set, coord_file, include_cpcmc_flag, charge, multi)

        input_file += "$NEW_JOB\n"

        input_file += generate_isc_blocks(nroots, sroot, troot, -1, isc_ishess, isc_fshess, usej, temp, dele, functional, basis_set, coord_file, include_cpcmc_flag, charge, multi)

    
    elif method in ["OPT", "OPT FREQ", "OPT NUMFREQ"]:
        nroots = get_numeric_input("Number of TDDFT roots", default=1)
        iroot = get_numeric_input("Root to optimize (IRoot)", default=1)
        iroot_mult = get_input("IRootMult (Singlet/Triplet)", default="Singlet")
        maxiter = get_numeric_input("maximum of iteration", default=100)
        input_file += generate_dft_block(method, nroots, iroot, iroot_mult, maxiter, functional, basis_set, coord_file, include_cpcmc_flag, include_tddft_flag, charge, multi)
    
    elif method in ["NEB", "NEB-CI", "NEB-TS", "FAST-NEB-TS", "LOOSE-NEB-TS", "TIGHT-NEB-TS"]:
        nroots = get_numeric_input("Number of TDDFT roots", default=1)
        iroot = get_numeric_input("Root to optimize (IRoot)", default=1)
        iroot_mult = get_input("IRootMult (Singlet/Triplet)", default="Singlet")
        maxiter = get_numeric_input("maximum of iteration", default=100)
        product_file = get_input("Specify NEB final XYZ filename", default="product.xyz")
        NIm = get_numeric_input("Number of images without fixed endpoints", default=8)
        Plevel = get_numeric_input("numbers (<=4) for more detailed printout",default=3)
        input_file += generate_neb_block(method, nroots, iroot, iroot_mult, maxiter, functional, basis_set, coord_file, include_cpcmc_flag, include_tddft_flag, product_file, NIm, Plevel, charge, multi)
        
    # Write input file to a file
    input_name = get_input("Specify input file name", default="opt_s0.inp")
    with open(input_name, 'w') as f:
        f.write(input_file)

    print(f"Input file '{input_name}' has been created.")

if __name__ == "__main__":
    main()
