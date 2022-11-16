
# ![Stenography Toolbox](img/title_small.png)

A toolbox for steganography:

- [x] Hide file in image
- [ ] Hide file in audio

## Requirements

```
python -m pip install -r requirements.txt
```

## Demo

### Hide text in image

![usage hide](img/usage_hide.png)

Input image:

![input image](test/pexels-johannes-plenio-1146706.jpg)

Input text:

```
Hello, World!
EOF
```

Output image:

![output image](test/tree.png)

![usage seek](img/usage_seek.png)

Extrated text:

[extracted.txt](test/extracted.txt)

```
Hello, World!

Hello, World!

Hello, World!

Hello, World!

Hello, World!

Hello, World!

Hello, Wor...
```
