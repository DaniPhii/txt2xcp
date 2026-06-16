# Casio fx-CP400 character sets

As of 2026/06/16, [the corresponding Wikipedia article](https://en.wikipedia.org/wiki/Casio_calculator_character_sets "Casio calculator character sets") doesn't include details about the character sets for the Casio ClassPad II (fx-CP400). So, I decided to work on this myself and try to create the correct character maps, even though the SDK for this specific device hasn't been published yet.

I tried using different encodings to avoid making a specific conversion table, i.e. CP437, Shift-JIS and UTF-16LE, but I got even worse mojibake effects, so I decided making my own conversion tables, which are down below.

The corresponding mapping is used in `classpad_encoder.py`.

### Code charts

**Character set with no prefix**

|     |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  **0x** |  <span style="display:inline-block; border:1px dashed;">␀</span>  |     |     |     |     |     |     |     |     |     |  <span style="display:inline-block; border:1px dashed;">␊</span>  |     |     |  <span style="display:inline-block; border:1px dashed;">␍</span>  |     |     |
|  **1x** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **2x** |  <span style="display:inline-block; border:1px dashed;">␠</span>  |  \!  |  \"  |  \#  |  \$  |  \%  |  \&  |  \'  |  \(  |  \)  |  \*  |  \+  |  \,  |  \-  |  \.  |  /  |
|  **3x** |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  \:  |  \;  |  \<  |  \=  |  \>  |  \?  |
|  **4x** |  \@  |  A  |  B  |  C  |  D  |  E  |  F  |  G  |  H  |  I  |  J  |  K  |  L  |  M  |  N  |  O  |
|  **5x** |  P  |  Q  |  R  |  S  |  T  |  U  |  V  |  W  |  X  |  Y  |  Z  |  \[  |  \  |  \]  |  \^  |  \_  |
|  **6x** |  \`  |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |  i  |  j  |  k  |  l  |  m  |  n  |  o  |
|  **7x** |  p  |  q  |  r  |  s  |  t  |  u  |  v  |  w  |  x  |  y  |  z  |  \{  |  \|  |  \}  |  \~  |     |
|  **8x** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **9x** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Ax** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Bx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Cx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Dx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Ex** |     |     |     |     |     |     |     |     |     |     |     |     |  <span style="display:inline-block; border:1px dashed;">$\vcenter{\small ᴇᴄ}$</span> |  <span style="display:inline-block; border:1px dashed;">$\vcenter{\small ᴇᴅ}$</span> |  <span style="display:inline-block; border:1px dashed;">$\vcenter{\small ᴇᴇ}$</span> |     |
|  **Fx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

**Character set with prefix 0xEC**

|     |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  **0x** |     |  À  |  Á  |  Â  |  Ã  |  Ä  |  Å  |  Æ  |  Ç  |  È  |  É  |  Ê  |  Ë  |  Ì  |  Í  |  Î  |
|  **1x** |  Ï  |  Ð  |  Ñ  |  Ò  |  Ó  |  Ô  |  Õ  |  Ö  |  Ø  |  Ù  |  Ú  |  Û  |  Ü  |  Ý  |  Þ  |  ẞ  |
|  **2x** |  Ÿ  |  Ā  |  Ă  |  Ą  |  Ć  |  Ĉ  |  Ċ  |  Č  |  Ď  |  Đ  |  Ē  |  Ĕ  |  Ė  |  Ę  |  Ě  |  Ĝ  |
|  **3x** |  Ğ  |  Ġ  |  Ģ  |  Ĥ  |  Ħ  |  Ĩ  |  Ī  |  Ĭ  |  Į  |  İ  |  Ĳ  |  Ĵ  |  Ķ  |  Ĺ  |  Ļ  |  Ľ  |
|  **4x** |  Ŀ  |  Ł  |  Ń  |  Ņ  |  Ň  |  Ŋ  |  Ō  |  Ŏ  |  Ő  |  Œ  |  Ŕ  |  Ŗ  |  Ř  |  Ś  |  Ŝ  |  Ş  |
|  **5x** |  Š  |  Ţ  |  Ť  |  Ŧ  |  Ũ  |  Ū  |  Ŭ  |  Ů  |  Ű  |  Ų  |  Ŵ  |  Ŷ  |  Ź  |  Ż  |  Ž  |  Ơ  |
|  **6x** |  Ư  |  Ǎ  |  Ǐ  |  Ǒ  |  Ǔ  |  Ǖ  |  Ǘ  |  Α  |  Β  |  Γ  |  Δ  |  Ε  |  Ζ  |  Η  |  Θ  |  Ι  |
|  **7x** |  Κ  |  Λ  |  Μ  |  Ν  |  Ξ  |  Ο  |  Π  |  Ρ  |  Σ  |  Τ  |  Υ  |  Φ  |  Χ  |  Ψ  |  Ω  |  А  |
|  **8x** |  Б  |  В  |  Г  |  Д  |  Е  |  Ё  |  Ж  |  З  |  И  |  Й  |  К  |  Л  |  М  |  Н  |  О  |  П  |
|  **9x** |  Р  |  С  |  Т  |  У  |  Ф  |  Х  |  Ц  |  Ч  |  Ш  |  Щ  |  Ъ  |  Ы  |  Ь  |  Э  |  Ю  |  Я  |
|  **Ax** |  Є  |  𝑨  |  𝑩  |  𝑪  |  𝑫  |  𝑬  |  𝑭  |  𝑮  |  𝑯  |  𝑰  |  𝑱  |  𝑲  |  𝑳  |  𝑴  |  𝑵  |  𝑶  |
|  **Bx** |  𝑷  |  𝑸  |  𝑹  |  𝑺  |  𝑻  |  𝑼  |  𝑽  |  𝑾  |  𝑿  |  𝒀  |  𝒁  |     |     |     |     |     |
|  **Cx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Dx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Ex** |  $\vcenter{\tiny 𝟢}$  |  $\vcenter{\tiny 𝟣}$  |  $\vcenter{\tiny 𝟤}$  |  $\vcenter{\tiny 𝟥}$  |  $\vcenter{\tiny 𝟦}$  |  $\vcenter{\tiny 𝟧}$  |  $\vcenter{\tiny 𝟨}$  |  $\vcenter{\tiny 𝟩}$  |  $\vcenter{\tiny 𝟪}$  |  $\vcenter{\tiny 𝟫}$  |  $\vcenter{﹢}$  |  $\vcenter{﹣}$  |     |     |     |     |
|  **Fx** |  ₀  |  ₁  |  ₂  |  ₃  |  ₄  |  ₅  |  ₆  |  ₇  |  ₈  |  ₉  |  ₊  |  ₋  |  ₋₁ |  ₘ  |  ₙ  |     |

**Character set with prefix 0xED**

|     |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  **0x** |     |  à  |  á  |  â  |  ã  |  ä  |  å  |  æ  |  ç  |  è  |  é  |  ê  |  ë  |  ì  |  í  |  î  |
|  **1x** |  ï  |  ð  |  ñ  |  ò  |  ó  |  ô  |  õ  |  ö  |  ø  |  ù  |  ú  |  û  |  ü  |  ý  |  þ  |  ß  |
|  **2x** |  ÿ  |  ā  |  ă  |  ą  |  ć  |  ĉ  |  ċ  |  č  |  ď  |  đ  |  ē  |  ĕ  |  ė  |  ę  |  ě  |  ĝ  |
|  **3x** |  ğ  |  ġ  |  ģ  |  ĥ  |  ħ  |  ĩ  |  ī  |  ĭ  |  į  |  ı  |  ĳ  |  ĵ  |  ķ  |  ĺ  |  ļ  |  ľ  |
|  **4x** |  ŀ  |  ł  |  ń  |  ņ  |  ň  |  ŋ  |  ō  |  ŏ  |  ő  |  œ  |  ŕ  |  ŗ  |  ř  |  ś  |  ŝ  |  ş  |
|  **5x** |  š  |  ţ  |  ť  |  ŧ  |  ũ  |  ū  |  ŭ  |  ů  |  ű  |  ų  |  ŵ  |  ŷ  |  ź  |  ż  |  ž  |  ơ  |
|  **6x** |  ư  |  ǎ  |  ǐ  |  ǒ  |  ǔ  |  ǖ  |  ǘ  |  α  |  β  |  γ  |  δ  |  ε  |  ζ  |  η  |  θ  |  ι  |
|  **7x** |  κ  |  λ  |  μ  |  ν  |  ξ  |  ο  |  π  |  ρ  |  σ  |  τ  |  υ  |  φ  |  χ  |  ψ  |  ω  |  а  |
|  **8x** |  б  |  в  |  г  |  д  |  е  |  ё  |  ж  |  з  |  и  |  й  |  к  |  л  |  м  |  н  |  о  |  п  |
|  **9x** |  р  |  с  |  т  |  у  |  ф  |  х  |  ц  |  ч  |  ш  |  щ  |  ъ  |  ы  |  ь  |  э  |  ю  |  я  |
|  **Ax** |  є  |  𝒂  |  𝒃  |  𝒄  |  𝒅  |  𝒆  |  𝒇  |  𝒈  |  𝒉  |  𝒊  |  𝒋  |  𝒌  |  𝒍  |  𝒎  |  𝒏  |  𝒐  |
|  **Bx** |  𝒑  |  𝒒  |  𝒓  |  𝒔  |  𝒕  |  𝒖  |  𝒗  |  𝒘  |  𝒙  |  𝒚  |  𝒛  |     |     |     |     |     |
|  **Cx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Dx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Ex** |  ς  |  ′  |  ″  |  ‴  |  ⁽  |  ⁾  |  ₓ  |  &#x209E;  |  ᵢ  |  ⱼ  |  ₖ  |     |     |     |     |     |
|  **Fx** |  ⁰  |  ¹  |  ²  |  ³  |  ⁴  |  ⁵  |  ⁶  |  ⁷  |  ⁸  |  ⁹  |  ⁺  |  ⁻  |  ⁻¹ |  ˣ  |  ʸ  |     |

**Character set prefixed with 0xEE**

|     |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  A  |  B  |  C  |  D  |  E  |  F  |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|  **0x** |     |  𝒾  |  ℯ  |  ᴇ  |  𝜋  |  ∞  |  °  |  ʳ  |  ᵀ  |  ʼ  |  ₙ  |  ∠  |  x̄ |  ȳ |  p̂  |  ⇒  |
|  **1x** |  ×  |  ≠  |  ≤  |  ≥  |  ±  |  ÷  |  ≒  |  ≪  |  ≫  |  ∈  |  ∋  |  ⊆  |  ⊇  |  ⊂  |  ⊃  |  ⋃  |
|  **2x** |  ⋂  |  ∟  |  ∨  |  ∀  |  ∧  |  ⊥  |  ≡  |  ∇  |  ▽  |  △  |  ∵  |  ∴  |  ‘  |  ’  |  ”  |  “  |
|  **3x** |  ⏎  |  ◢  |  ˗  |  ℕ  |  ℤ  |  ℚ  |  ℝ  |  ℂ  |  ¨  |  ˊ  |  ˋ  |  ˆ  |  ˜  |  ˚  |  ª  |  º  |
|  **4x** |  ∓  |  ≈  |  ⇔  |  ∃  |  ∉  |  ⊄  |  ⊈  |  ∌  |  ⊅  |  ⊉  |     |  ⨲  |  ∾  |  ≅  |  ≢  |  ∝  |
|  **5x** |  √  |  ∑  |  ∏  |  ∫  |  ∬  |  ∮  |  ∂  |  ¿  |  ¡  |  ¢  |  £  |  ¥  |  ₣  |  Ꞙ  |  €  |  ⨍  |
|  **6x** |  Å  |  ℃  |  ℉  |  ←︎  |  ↑︎  |  →︎  |  ↓︎  |  ↔︎  |  ↕︎  |  ↖︎  |  ↗︎  |  ↘︎  |  ↙︎  |  ¼  |  ½  |  ¾  |
|  **7x** |  §  |  ※  |  ¶  |  ¤  |  ∥  |  ¦  |  【  |  】  |  ⊿  |  ♪  |  ♫  |  🔒︎  |  🔓︎  |  □  |  ■  |  ☑︎  |
|  **8x** |  ♠  |  ♣  |  ♥  |  ♦  |  ◇  |  ▲︎  |  ▶︎  |  ▼︎  |  ◀︎  |  ○  |  ◎  |  ◉  |  ●  |  ©  |  ®  |  …  |
|  **9x** |  ⋯  |  ∘  |  ∙  |  ∗  |  ⮣  |  ⮧  |  ⮡  |  ⮥  |  ☒  |  🔔︎  |     |  🞄  |  ⇧  |  ⭡  |  ⮌  |  ⏨  |
|  **Ax** |  ⛭  |  ⭠  |  ⊕  |  ⊖  |  ⊗  |  ⊘  |  ∦  |  ⫽  |  z̄ |  Ā  |  B̄ |  P̄ |  Q̄ |  ⸬  |  ﹐  |  𝒿  |
|  **Bx** |  ⚙︎  |     |     |  ᴀ  |  ʙ  |  ᴊ  |  ᴋ  |  ɴ  |  ᴘ  |  𝖾  |  𝗉  |  𝗎  |  𝝁  |  𝝉  |  ∞  |  🮠  |
|  **Cx** |  <span style="display:none">📟︎</span>  | <span style="display:none">$\tiny{\sqrt{μ₀/ε₀}}$</span>  |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Dx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Ex** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|  **Fx** |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

## Previous notes from SnailMath shared on 2020/11/22:

> I programmed this a few month ago, I didn't intended to publish that at that time. These are the notes I took about the file format casio uses.
> The variable on the calc will be called 'file', because I didn't bother to adjust the checksum for different filenames.
> I exported different files from the calculator (actually the cp manager) and compared the hexdump of them until I found this out:
> 
> ```
> 
> 0x4b length
> 
> 0x61: length+3
> 0x62: length next digits (little endian)
> 
> 0x6e: content of the file in blocks of 4 bytes
> 
> after the content:
> 00ff
> 
> 0-3 bytes filled with 00 , fill until address kongruent to 0 mod 4
> 
> at next location kongruent to 1 mod 4:
> 2 bytes checksum
> eof
> 
> 
> 
> i know how to generate this
> |
> | no of bytes
> |   |          offset in the file
> |   |     +---------+
> |   |     |         |
> *  0x48   0x00 - 0x47 : always the same
> +  0x04   0x48 - 0x4b : length + 0x12 & ~0x03  big endian
> *  0x0d   0x4c - 0x58 : "GUQ" + 0xff
> +  0x08   0x59 - 0x60 : 8 digits ascii    length + 0x12 & ~0x03
> *  0x0d   0x61 - 0x6d : length + 3 in little endian, followed by 0x00
> *         0x6e -      : data
> *  0x02               : 0x00 0xff
> *  0-3                : ((0x01 - length) & 0x03) bytes of 0x00
>    0x02               : checksum
> 
> 
> ```
> 
> I tried different ways for calculatng the checksum (from including certin  values and not including certain values, until I got it working. First this worked only for files less than 9 byte long, but I found the bug. This will work with files up to 32000 bytes and even more. (I tested it with chapters of random ebooks I had lying around.)

