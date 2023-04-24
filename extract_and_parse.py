def parse_antibiotic_data(data: str):
    if data == "nip" or data.startswith("Missing BP"):
        return False
    return True


def extract_antibiotic_data(data: str):
    SIR_category = data[0]
    if "<" in data or ">" in data:
        return (None, SIR_category)
    else:
        MIC_value = float(
            "".join([char for char in data if char.isdigit() or char == "."])
        )
        return (MIC_value, SIR_category)
