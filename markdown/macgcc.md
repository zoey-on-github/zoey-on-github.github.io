---
title: examining the macOS gcc binary
---
if you've ever written C(or c++) on a mac, you'll know that the so-called `gcc` is just clang in disguise<br>
```sh
$ gcc
clang: error: no input files
```
most people(fairly) assume that this is just an alias, but this is not true! it's a binary<br>
```sh
$ which gcc
/usr/bin/gcc
```
now, what *is* this binary? i naively assumed that it would just be shelling out to `clang` but it turns out the answer is more interesting than that<br>
```c
int sub_1000006c4(int arg0, int arg1) {
    r19 = arg1;
    r20 = arg0;
    if (*_mainExecutableToolName.once == -0x1) {
            if (*(int8_t *)*_mainExecutableToolName.toolName == 0x63 && *(int8_t *)(*_mainExecutableToolName.toolName + 0x1) == 0x63 && *(int8_t *)(*_mainExecutableToolName.toolName + 0x2) == 0x0) {
                    r21 = "clang";
            }
            else {
                    if (strcmp(*_mainExecutableToolName.toolName, "llvm-gcc") == 0x0) {
                            r21 = "clang";
                    }
                    else {
                            r21 = *_mainExecutableToolName.toolName;
                            if (strcmp(*_mainExecutableToolName.toolName, "c++") == 0x0 || strcmp(r21, "llvm-g++") == 0x0) {
                                    r21 = "clang++";
                            }
                    }
            }
            xcselect_invoke_xcrun();
    }
    while (true) {
            dispatch_once(_mainExecutableToolName.once, ___block_literal_global);
            if (*(int8_t *)*_mainExecutableToolName.toolName == 0x63) {
                    if (*(int8_t *)(*_mainExecutableToolName.toolName + 0x1) == 0x63) {
                            if (*(int8_t *)(*_mainExecutableToolName.toolName + 0x2) != 0x0) {
                                    if (strcmp(*_mainExecutableToolName.toolName, "llvm-gcc") == 0x0) {
                                            r21 = "clang";
                                    }
                                    else {
                                            if (strcmp(*_mainExecutableToolName.toolName, "c++") != 0x0) {
                                                    r21 = *_mainExecutableToolName.toolName;
                                                    if (strcmp(*_mainExecutableToolName.toolName, "llvm-g++") == 0x0) {
                                                            r21 = "clang++";
                                                    }
                                            }
                                            else {
                                                    r21 = "clang++";
                                            }
                                    }
                                    xcselect_invoke_xcrun();
                            }
                            else {
                                    xcselect_invoke_xcrun();
                            }
                    }
                    else {
                            if (strcmp(*_mainExecutableToolName.toolName, "llvm-gcc") == 0x0) {
                                    r21 = "clang";
                            }
                            else {
                                    if (strcmp(*_mainExecutableToolName.toolName, "c++") != 0x0) {
                                            r21 = *_mainExecutableToolName.toolName;
                                            if (strcmp(*_mainExecutableToolName.toolName, "llvm-g++") == 0x0) {
                                                    r21 = "clang++";
                                            }
                                    }
                                    else {
                                            r21 = "clang++";
                                    }
                            }
                            xcselect_invoke_xcrun();
                    }
            }
            else {
                    if (strcmp(*_mainExecutableToolName.toolName, "llvm-gcc") == 0x0) {
                            r21 = "clang";
                    }
                    else {
                            if (strcmp(*_mainExecutableToolName.toolName, "c++") != 0x0) {
                                    r21 = *_mainExecutableToolName.toolName;
                                    if (strcmp(*_mainExecutableToolName.toolName, "llvm-g++") == 0x0) {
                                            r21 = "clang++";
                                    }
                            }
                            else {
                                    r21 = "clang++";
                            }
                    }
                    xcselect_invoke_xcrun();
            }
            continue;
    }
}
```
there's some interesting stuff here(for example special logic for checking if it's being run as c++ or llvm-gcc specifically), but the key thing we're interested in is this line of code:<br>
```c
xcselect_invoke_xcrun()
 ```
this is a function from libxcselect.dylib, but it's basically the same thing as running `xcrun`(in fact: [the xcrun binary basically just calls this function](https://zoey-on-github.github.io/Screenshot_2026-10-21_at_1.26.54_AM.png)) <br>
but that raises the important question: what does xcrun *do*? i've certainly never heard of it before this<br>
well, checking [the manpage](https://keith.github.io/xcode-man-pages/xcrun.1.html) we can see that it calls developer tools from the developer tool directory. [all the developer tools that xcode-select installs on macOS are actually just being run through xcrun.](https://zoey-on-github.github.io/Screenshot_2026-10-21_at_12.57.05_PM.png)^[if you're wondering *why* this is, my guess is because of SIP. /usr/bin is a protected directory on macOS and i assume apple can't update it without requiring a restart, and you can update the xcode tools without having to restart your mac. as for why they dont just add the developer tools directory to path, my guess is that they want the freedom to change this directory whenever they want] this gives us an important bit of info: the location of the *actual* gcc binary that's being called. thankfully for us, there is a `--find` command that can give us exactly this.<br>
```sh
$ xcrun --find gcc
/Library/Developer/CommandLineTools/usr/bin/gcc
```
looking in this directory, we can see that c++, g++, clang++, llvm-gcc and cc are just alises to the `gcc` binary that's in the same directory:<br>
![](images/Screenshot_2026-10-21_at_1.11.00_PM.png) ![](images/Screenshot_2026-10-21_at_1.11.10_PM.png)<br>
well, what does *that* gcc binary do, then?<br>
opening it in my disassembler, we see that it... shells out to xcrun and calls clang(or clang++ depending on how it's called) <br>
```C
int EntryPoint(int arg0, int arg1) {
    r22 = arg1;
    r21 = arg0;
    asm { sbfiz      x8, x21, #0x3, #0x20 };
    r0 = malloc(r8 + 0x10);
    if (r0 == 0x0) {
            err(0x47, r1);
    }
    r19 = r0;
    *r0 = "/usr/bin/xcrun";
    r23 = *r22;
    r0 = strlen(r23);
    if (*(int8_t *)(r23 + (r0 - 0x1 << r64)) == 0x2b && *(int8_t *)(r23 + (r0 - 0x2 << r64)) == 0x2b) {
            r8 = "clang++";
    }
    else {
            r8 = "clang";
    }
    r19[0x1] = r8;
    if (r21 >= 0x2) {
            asm { ubfiz      x2, x8, #0x3, #0x20 };
            memcpy(r19 + 0x10, r22 + 0x8, r2);
            r8 = r21;
    }
    else {
            r8 = 0x1;
    }
    *(r19 + r8 * 0x8 + 0x8) = 0x0;
    r0 = execv("/usr/bin/xcrun", r19);
    err(0x47, r1);
    return r0;
}
```
<br>
