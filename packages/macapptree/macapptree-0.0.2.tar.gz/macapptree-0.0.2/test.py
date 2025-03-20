from macapptree import get_tree, get_app_bundle, get_tree_screenshot
import json
# # import unidecode

# calculator = "com.apple.calculator"
# clear_vpn = "com.macpaw.clearvpn.macos-setapp"

# # tree = get_tree(clear_vpn)

# # with open("out.json", "w") as f:
# #     json.dump(tree, f) 

# def unicode_escape(s):
#     return "".join(map(lambda c: rf"\u{ord(c):04x}", s))


# # print(u"\u043a\u043d\u043e\u043f\u043a\u0430")
# # print(unicode_escape("Австралія"))

# s = "\u0410\u0432\u0441\u0442\u0440\u0456\u044f"
# print(str(s))

# # print(unidecode.unidecode("\u043a\u043d\u043e\u043f\u043a\u0430"))

# # print(tree)


# bundle = "zoom"
bundle = get_app_bundle("BusyCal")

tree, im, im_seg = get_tree_screenshot(bundle)

im.save("out.png")
im_seg.save("out_seg.png")

with open("out.json", "w") as f:
    json.dump(tree, f) 