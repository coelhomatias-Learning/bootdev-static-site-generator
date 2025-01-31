props = {
    "href": "https://www.google.com",
    "target": "_blank",
}

props_str = " ".join(map(lambda x: f'{x[0]}="{x[1]}"', props.items()))
print(props_str)
