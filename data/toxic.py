from constants import p_hab, p_earth

toxic = { # IDLH of compounds
	'CO': 1.2e-3,
	'NO': 1e-4, # https://www.cdc.gov/niosh/npg/npgd0448.html
	'SO2': 1e-4,
	'HCl': 5e-5,
	'PH3': 5e-5,
	'HF': 3e-5,
	'NO2': 2e-5
}


def istox(p) -> bool:
	if p.atm and p.atm > p_hab[0]:
		if 'O2' not in p.atmosphere or p.atmosphere['O2']*p.atm < p_hab[0]:
			return True
		for chem in toxic:
			if chem in p.atmosphere and p.atmosphere[chem]*p.atm > toxic[chem]*p_earth:
				return True
	return False
