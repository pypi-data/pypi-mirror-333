import subprocess

## Check seurat not installed

try:
	output = subprocess.check_output(
		["Rscript", "--vanilla", "sc_ssGSEA/load_seurat.R"],
		stderr = subprocess.STDOUT
	).decode()
except subprocess.CalledProcessError as exc:
	output = exc.output.decode()

if "there is no package" in output:
	print((
		f"ERROR: Seurat was not found. To input an RDS file, please install "
		f"Seurat in this environment.\nSee instructions at "
		f"https://satijalab.org/seurat/articles/install.html"
	))

## Check R (command) not available

print("\n\n")

try:
	output = subprocess.check_output(
		["asdf", "asdfasf"],
		stderr = subprocess.STDOUT
	).decode()
except FileNotFoundError:
	print((
		f"ERROR: R not found. To input an RDS file, please install R and "
		f"the Seurat package.\n\tR installation: https://cran.r-project.org/mirrors.html\n\t" 
		f"Seurat installation: https://satijalab.org/seurat/articles/install.html"
	))

print(output)
