from pyrogram.types import InlineKeyboardButton

[
    [
        InlineKeyboardButton(text='Test1', url='http://a.co/'),
        InlineKeyboardButton(text='Add Column', callback_data='add_c_0_1')
    ],
    [
        InlineKeyboardButton(text='Test2', url='http://B.co/'),
        InlineKeyboardButton(text='Test 2 2', url='http://a.co/'),
        InlineKeyboardButton(text='Test 2 3', url='http://A.co/'),
        InlineKeyboardButton(text='Test 2 4', url='http://a.co/'),
        InlineKeyboardButton(text='Test 2 5', url='http://a.co/'),
        InlineKeyboardButton(text='Test 2 6', url='http://a.co/'),
        InlineKeyboardButton(text='Test 2 7', url='http://a.co/')
    ],
    [
        InlineKeyboardButton(text='Test 3', url='http://Example.com/'),'add_c_2_1'
    ],
    [
        InlineKeyboardButton(text='Add Row', callback_data='add_r_3')
    ]
]
