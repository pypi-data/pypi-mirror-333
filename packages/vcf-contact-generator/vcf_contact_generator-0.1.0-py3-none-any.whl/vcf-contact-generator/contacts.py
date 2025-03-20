def create_single_contact(filepath, name, phone):
    if not filepath or not isinstance(filepath, str):
        raise ValueError("Filepath must be a non-empty string")
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    if not phone or not isinstance(phone, str):
        raise ValueError("Phone must be a non-empty string")
    
    name = name.strip()
    phone = phone.strip()
    filepath = filepath.strip()
    
    if not filepath.endswith('.vcf'):
        filepath = filepath.rstrip('.').rstrip('.txt').rstrip('.vcf') + '.vcf'
    
    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
N:;{name};;;
FN:{name}
TEL;TYPE=CELL:{phone}
END:VCARD\n"""
    
    try:
        with open(filepath, 'a', encoding='utf-8') as file:
            file.write(vcard_content)
            
    except IOError as e:
        raise IOError(f"Error saving contact to file: {e}")
    
    return f"Contact '{name}' has been created successfully in {filepath}"


def create_library(filepath, contacts):
    if not filepath or not isinstance(filepath, str):
        raise ValueError("Filepath must be a non-empty string")
    if not isinstance(contacts, list) or not all(isinstance(c, tuple) and len(c) == 2 for c in contacts):
        raise ValueError("Contacts must be a list of tuples (name, phone)")
    
    filepath = filepath.strip()
    
    if not filepath.endswith('.vcf'):
        filepath = filepath.rstrip('.').rstrip('.txt').rstrip('.vcf') + '.vcf'

    open(filepath, 'w').close()
    
    try:
        for name, phone in contacts:
            create_single_contact(filepath, name, phone)
    
    except IOError as e:
        raise IOError(f"Error saving contacts to file: {e}")

    return f"{len(contacts)} contacts have been created in {filepath}"




contacts_list = [
    ("example", "111222333"),
    ("example2", "444555666"),
]

print(create_library("phone_numbers.vcf", contacts_list))