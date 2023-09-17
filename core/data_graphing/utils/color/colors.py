import enum


# Colors taken from : https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors
class Color(enum.Enum):
    # region Google Colour Palette
    # region RED
    RED_50 = (255, 235, 238)
    RED_100 = (255, 205, 210)
    RED_200 = (239, 154, 154)
    RED_300 = (229, 115, 115)
    RED_400 = (239, 83, 80)
    RED_500 = (244, 67, 54)
    RED_600 = (229, 57, 53)
    RED_700 = (211, 47, 47)
    RED_800 = (198, 40, 40)
    RED_900 = (183, 28, 28)
    RED_A100 = (255, 138, 128)
    RED_A200 = (255, 82, 82)
    RED_A400 = (255, 23, 68)
    RED_A700 = (213, 0, 0)
    # endregion RED

    # region PINK
    PINK_50 = (252, 228, 236)
    PINK_100 = (248, 187, 208)
    PINK_200 = (244, 143, 177)
    PINK_300 = (240, 98, 146)
    PINK_400 = (236, 64, 122)
    PINK_500 = (233, 30, 99)
    PINK_600 = (216, 27, 96)
    PINK_700 = (194, 24, 91)
    PINK_800 = (173, 20, 87)
    PINK_900 = (136, 14, 79)
    PINK_A100 = (255, 128, 171)
    PINK_A200 = (255, 64, 129)
    PINK_A400 = (245, 0, 87)
    PINK_A700 = (197, 17, 98)
    # endregion PINK

    # region PURPLE
    PURPLE_50 = (243, 229, 245)
    PURPLE_100 = (225, 190, 231)
    PURPLE_200 = (206, 147, 216)
    PURPLE_300 = (186, 104, 200)
    PURPLE_400 = (171, 71, 188)
    PURPLE_500 = (156, 39, 176)
    PURPLE_600 = (142, 36, 170)
    PURPLE_700 = (123, 31, 162)
    PURPLE_800 = (106, 27, 154)
    PURPLE_900 = (74, 20, 140)
    PURPLE_A100 = (234, 128, 252)
    PURPLE_A200 = (224, 64, 251)
    PURPLE_A400 = (213, 0, 249)
    PURPLE_A700 = (170, 0, 255)
    # endregion PURPLE

    # region DEEPPURPLE
    DEEPPURPLE_50 = (237, 231, 246)
    DEEPPURPLE_100 = (209, 196, 233)
    DEEPPURPLE_200 = (179, 157, 219)
    DEEPPURPLE_300 = (149, 117, 205)
    DEEPPURPLE_400 = (126, 87, 194)
    DEEPPURPLE_500 = (103, 58, 183)
    DEEPPURPLE_600 = (94, 53, 177)
    DEEPPURPLE_700 = (81, 45, 168)
    DEEPPURPLE_800 = (69, 39, 160)
    DEEPPURPLE_900 = (49, 27, 146)
    DEEPPURPLE_A100 = (179, 136, 255)
    DEEPPURPLE_A200 = (124, 77, 255)
    DEEPPURPLE_A400 = (101, 31, 255)
    DEEPPURPLE_A700 = (98, 0, 234)
    # endregion DEEPPURPLE

    # region INDIGO
    INDIGO_50 = (232, 234, 246)
    INDIGO_100 = (197, 202, 233)
    INDIGO_200 = (159, 168, 218)
    INDIGO_300 = (121, 134, 203)
    INDIGO_400 = (92, 107, 192)
    INDIGO_500 = (63, 81, 181)
    INDIGO_600 = (57, 73, 171)
    INDIGO_700 = (48, 63, 159)
    INDIGO_800 = (40, 53, 147)
    INDIGO_900 = (26, 35, 126)
    INDIGO_A100 = (140, 158, 255)
    INDIGO_A200 = (83, 109, 254)
    INDIGO_A400 = (61, 90, 254)
    INDIGO_A700 = (48, 79, 254)
    # endregion INDIGO

    # region BLUE
    BLUE_50 = (227, 242, 253)
    BLUE_100 = (187, 222, 251)
    BLUE_200 = (144, 202, 249)
    BLUE_300 = (100, 181, 246)
    BLUE_400 = (66, 165, 245)
    BLUE_500 = (33, 150, 243)
    BLUE_600 = (30, 136, 229)
    BLUE_700 = (25, 118, 210)
    BLUE_800 = (21, 101, 192)
    BLUE_900 = (13, 71, 161)
    BLUE_A100 = (130, 177, 255)
    BLUE_A200 = (68, 138, 255)
    BLUE_A400 = (41, 121, 255)
    BLUE_A700 = (41, 98, 255)
    # endregion BLUE

    # region LIGHTBLUE
    LIGHTBLUE_50 = (225, 245, 254)
    LIGHTBLUE_100 = (179, 229, 252)
    LIGHTBLUE_200 = (129, 212, 250)
    LIGHTBLUE_300 = (79, 195, 247)
    LIGHTBLUE_400 = (41, 182, 246)
    LIGHTBLUE_500 = (3, 169, 244)
    LIGHTBLUE_600 = (3, 155, 229)
    LIGHTBLUE_700 = (2, 136, 209)
    LIGHTBLUE_800 = (2, 119, 189)
    LIGHTBLUE_900 = (1, 87, 155)
    LIGHTBLUE_A100 = (128, 216, 255)
    LIGHTBLUE_A200 = (64, 196, 255)
    LIGHTBLUE_A400 = (0, 176, 255)
    LIGHTBLUE_A700 = (0, 145, 234)
    # endregion LIGHTBLUE

    # region CYAN
    CYAN_50 = (224, 247, 250)
    CYAN_100 = (178, 235, 242)
    CYAN_200 = (128, 222, 234)
    CYAN_300 = (77, 208, 225)
    CYAN_400 = (38, 198, 218)
    CYAN_500 = (0, 188, 212)
    CYAN_600 = (0, 172, 193)
    CYAN_700 = (0, 151, 167)
    CYAN_800 = (0, 131, 143)
    CYAN_900 = (0, 96, 100)
    CYAN_A100 = (132, 255, 255)
    CYAN_A200 = (24, 255, 255)
    CYAN_A400 = (0, 229, 255)
    CYAN_A700 = (0, 184, 212)
    # endregion CYAN

    # region TEAL
    TEAL_50 = (224, 242, 241)
    TEAL_100 = (178, 223, 219)
    TEAL_200 = (128, 203, 196)
    TEAL_300 = (77, 182, 172)
    TEAL_400 = (38, 166, 154)
    TEAL_500 = (0, 150, 136)
    TEAL_600 = (0, 137, 123)
    TEAL_700 = (0, 121, 107)
    TEAL_800 = (0, 105, 92)
    TEAL_900 = (0, 77, 64)
    TEAL_A100 = (167, 255, 235)
    TEAL_A200 = (100, 255, 218)
    TEAL_A400 = (29, 233, 182)
    TEAL_A700 = (0, 191, 165)
    # endregion TEAL

    # region GREEN
    GREEN_50 = (232, 245, 233)
    GREEN_100 = (200, 230, 201)
    GREEN_200 = (165, 214, 167)
    GREEN_300 = (129, 199, 132)
    GREEN_400 = (102, 187, 106)
    GREEN_500 = (76, 175, 80)
    GREEN_600 = (67, 160, 71)
    GREEN_700 = (56, 142, 60)
    GREEN_800 = (46, 125, 50)
    GREEN_900 = (27, 94, 32)
    GREEN_A100 = (185, 246, 202)
    GREEN_A200 = (105, 240, 174)
    GREEN_A400 = (0, 230, 118)
    GREEN_A700 = (0, 200, 83)
    # endregion GREEN

    # region LIGHTGREEN
    LIGHTGREEN_50 = (241, 248, 233)
    LIGHTGREEN_100 = (220, 237, 200)
    LIGHTGREEN_200 = (197, 225, 165)
    LIGHTGREEN_300 = (174, 213, 129)
    LIGHTGREEN_400 = (156, 204, 101)
    LIGHTGREEN_500 = (139, 195, 74)
    LIGHTGREEN_600 = (124, 179, 66)
    LIGHTGREEN_700 = (104, 159, 56)
    LIGHTGREEN_800 = (85, 139, 47)
    LIGHTGREEN_900 = (51, 105, 30)
    LIGHTGREEN_A100 = (204, 255, 144)
    LIGHTGREEN_A200 = (178, 255, 89)
    LIGHTGREEN_A400 = (118, 255, 3)
    LIGHTGREEN_A700 = (100, 221, 23)
    # endregion LIGHTGREEN

    # region LIME
    LIME_50 = (249, 251, 231)
    LIME_100 = (240, 244, 195)
    LIME_200 = (230, 238, 156)
    LIME_300 = (220, 231, 117)
    LIME_400 = (212, 225, 87)
    LIME_500 = (205, 220, 57)
    LIME_600 = (192, 202, 51)
    LIME_700 = (175, 180, 43)
    LIME_800 = (158, 157, 36)
    LIME_900 = (130, 119, 23)
    LIME_A100 = (244, 255, 129)
    LIME_A200 = (238, 255, 65)
    LIME_A400 = (198, 255, 0)
    LIME_A700 = (174, 234, 0)
    # endregion LIME

    # region YELLOW
    YELLOW_50 = (255, 253, 231)
    YELLOW_100 = (255, 249, 196)
    YELLOW_200 = (255, 245, 157)
    YELLOW_300 = (255, 241, 118)
    YELLOW_400 = (255, 238, 88)
    YELLOW_500 = (255, 235, 59)
    YELLOW_600 = (253, 216, 53)
    YELLOW_700 = (251, 192, 45)
    YELLOW_800 = (249, 168, 37)
    YELLOW_900 = (245, 127, 23)
    YELLOW_A100 = (255, 255, 141)
    YELLOW_A200 = (255, 255, 0)
    YELLOW_A400 = (255, 234, 0)
    YELLOW_A700 = (255, 214, 0)
    # endregion YELLOW

    # region AMBER
    AMBER_50 = (255, 248, 225)
    AMBER_100 = (255, 236, 179)
    AMBER_200 = (255, 224, 130)
    AMBER_300 = (255, 213, 79)
    AMBER_400 = (255, 202, 40)
    AMBER_500 = (255, 193, 7)
    AMBER_600 = (255, 179, 0)
    AMBER_700 = (255, 160, 0)
    AMBER_800 = (255, 143, 0)
    AMBER_900 = (255, 111, 0)
    AMBER_A100 = (255, 229, 127)
    AMBER_A200 = (255, 215, 64)
    AMBER_A400 = (255, 196, 0)
    AMBER_A700 = (255, 171, 0)
    # endregion AMBER

    # region ORANGE
    ORANGE_50 = (255, 243, 224)
    ORANGE_100 = (255, 224, 178)
    ORANGE_200 = (255, 204, 128)
    ORANGE_300 = (255, 183, 77)
    ORANGE_400 = (255, 167, 38)
    ORANGE_500 = (255, 152, 0)
    ORANGE_600 = (251, 140, 0)
    ORANGE_700 = (245, 124, 0)
    ORANGE_800 = (239, 108, 0)
    ORANGE_900 = (230, 81, 0)
    ORANGE_A100 = (255, 209, 128)
    ORANGE_A200 = (255, 171, 64)
    ORANGE_A400 = (255, 145, 0)
    ORANGE_A700 = (255, 109, 0)
    # endregion ORANGE

    # region DEEPORANGE
    DEEPORANGE_50 = (251, 233, 231)
    DEEPORANGE_100 = (255, 204, 188)
    DEEPORANGE_200 = (255, 171, 145)
    DEEPORANGE_300 = (255, 138, 101)
    DEEPORANGE_400 = (255, 112, 67)
    DEEPORANGE_500 = (255, 87, 34)
    DEEPORANGE_600 = (244, 81, 30)
    DEEPORANGE_700 = (230, 74, 25)
    DEEPORANGE_800 = (216, 67, 21)
    DEEPORANGE_900 = (191, 54, 12)
    DEEPORANGE_A100 = (255, 158, 128)
    DEEPORANGE_A200 = (255, 110, 64)
    DEEPORANGE_A400 = (255, 61, 0)
    DEEPORANGE_A700 = (221, 44, 0)
    # endregion DEEPORANGE

    # region BROWN
    BROWN_50 = (239, 235, 233)
    BROWN_100 = (215, 204, 200)
    BROWN_200 = (188, 170, 164)
    BROWN_300 = (161, 136, 127)
    BROWN_400 = (141, 110, 99)
    BROWN_500 = (121, 85, 72)
    BROWN_600 = (109, 76, 65)
    BROWN_700 = (93, 64, 55)
    BROWN_800 = (78, 52, 46)
    BROWN_900 = (62, 39, 35)
    # endregion BROWN

    # region GREY
    GREY_50 = (250, 250, 250)
    GREY_100 = (245, 245, 245)
    GREY_200 = (238, 238, 238)
    GREY_300 = (224, 224, 224)
    GREY_400 = (189, 189, 189)
    GREY_500 = (158, 158, 158)
    GREY_600 = (117, 117, 117)
    GREY_700 = (97, 97, 97)
    GREY_800 = (66, 66, 66)
    GREY_900 = (33, 33, 33)
    # endregion GREY

    # region BLUEGREY
    BLUEGREY_50 = (236, 239, 241)
    BLUEGREY_100 = (207, 216, 220)
    BLUEGREY_200 = (176, 190, 197)
    BLUEGREY_300 = (144, 164, 174)
    BLUEGREY_400 = (120, 144, 156)
    BLUEGREY_500 = (96, 125, 139)
    BLUEGREY_600 = (84, 110, 122)
    BLUEGREY_700 = (69, 90, 100)
    BLUEGREY_800 = (55, 71, 79)
    BLUEGREY_900 = (38, 50, 56)
    # endregion BLUEGREY

    WHITE = (1, 1, 1)
    BLACK = (0, 0, 0)
    # endregion Google Colour Palette

    # region OTHER PALETTES
    # region PONYO
    PONYO_0 = (221, 237, 255)
    PONYO_1 = (37, 56, 125)
    PONYO_2 = (54, 69, 144)
    PONYO_3 = (49, 72, 153)
    PONYO_4 = (84, 131, 196)
    PONYO_5 = (98, 160, 220)
    PONYO_6 = (129, 180, 223)
    PONYO_7 = (102, 18, 37)
    PONYO_8 = (152, 67, 100)
    PONYO_9 = (176, 61, 55)
    # endregion PONYO

    # region KIKI
    KIKI_0 = (62, 152, 163)
    KIKI_1 = (33, 136, 168)
    KIKI_2 = (26, 60, 112)
    KIKI_3 = (24, 73, 162)
    KIKI_4 = (142, 135, 82)
    KIKI_5 = (213, 215, 112)
    KIKI_6 = (66, 64, 108)
    KIKI_7 = (203, 185, 178)
    KIKI_8 = (45, 8, 10)
    KIKI_9 = (194, 56, 65)
    # endregion KIKI

    # region SPIRITED AWAY
    SPIRIT_0 = (88, 165, 86)
    SPIRIT_1 = (47, 154, 141)
    SPIRIT_2 = (2, 41, 96)
    SPIRIT_3 = (0, 0, 0)
    SPIRIT_4 = (237, 227, 213)
    SPIRIT_5 = (115, 119, 123)
    SPIRIT_6 = (109, 57, 28)
    SPIRIT_7 = (146, 38, 47)
    SPIRIT_8 = (184, 61, 73)
    SPIRIT_9 = (223, 97, 103)
    # endregion SPIRITED AWAY

    # region CASTLE IN THE SKY
    CASTLE_0 = (117, 143, 191)
    CASTLE_1 = (47, 105, 193)
    CASTLE_2 = (48, 68, 54)
    CASTLE_3 = (78, 104, 60)
    CASTLE_4 = (120, 166, 112)
    CASTLE_5 = (137, 56, 54)
    CASTLE_6 = (167, 120, 76)
    CASTLE_7 = (153, 93, 52)
    CASTLE_8 = (229, 210, 52)
    CASTLE_9 = (218, 219, 109)
    # endregion CASTLE IN THE SKY

    # region WUBRG
    WUBRG_W = (0.87, 0.52, 0.32)
    WUBRG_U = (0.3, 0.45, 0.69)
    WUBRG_B = (0.15, 0.15, 0.15)
    WUBRG_R = (0.77, 0.31, 0.32)
    WUBRG_G = (0.33, 0.66, 0.41)
    # endregion WUBRG
    # region OTHER PALETTES
