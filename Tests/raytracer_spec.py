#!/usr/bin/env python
# -*- coding: utf-8 -*-
# John Loeber | July 12 2016 | Python 2.7.6 | contact@johnloeber.com

import unittest
from collections import OrderedDict
from contacts_rank import *

contact_1 = Contact(name="Quentin Query", nickname="queryman", email="qq@gmail.com", phone="8725922902")
contact_2 = Contact(name="Quentin Query", nickname="queryman", email="qq@gmail.com", phone="8725922902")
contact_3 = Contact(name="Quentin Query", nickname="queryman", email="qq@gmail.com", phone="8725922902")
contact_4 = Contact(name="Quentin Query", nickname="queryman", email="qq@gmail.com", phone="8725922902")
contact_5 = Contact(name="Barn", nickname="barn", email="barn@gmail.com", phone="8725922902")
contact_6 = Contact(name="Barn", nickname="barn", email="barn@bbmail.com", phone="8725922902")
contact_7 = Contact(name="Barn", nickname="barn", email="barn82@bbmail.com", phone="8272592202")
contact_8 = Contact(name="BARN", email="barn82@bbmail.com", phone="8272592282", nickname = "baRN")
contact_9 = Contact(name="QQ", email="qq@gmail.com")
contact_10 = Contact()
contact_11 = Contact(name="partial", phone="8009991000", email="@@", nickname="")
contact_12 = Contact(name="one entry")

class ContactsTests(unittest.TestCase):
    """ 
    Tests for contacts_rank.py
    """
    def test_clean_name(self):
        self.assertEqual(clean_name(" $@#  abc   "), "$@# abc")
        self.assertEqual(clean_name("      "), None)
        self.assertEqual(clean_name(None), None)
        self.assertEqual(clean_name(" Test FABC  "), "test fabc")
        self.assertEqual(clean_name(u'idzie wąż wąską dróżką'), u'idzie wąż wąską dróżką')
 
    def test_clean_email(self):
        self.assertEqual(clean_email("foo@gmail"), None)      
        self.assertEqual(clean_email("   FOOgmail.com"), None)      
        self.assertEqual(clean_email("    FOO@GMAIL.com"), "foo@gmail.com")      
        self.assertEqual(clean_email("FOO@GMAIL.com"), "foo@gmail.com")      
        self.assertEqual(clean_email("b@g.co"), "b@g.co")      
        self.assertEqual(clean_email("@g.c"), None)   
        self.assertEqual(clean_email("b@.c"), None)      
        self.assertEqual(clean_email("bg@gsd@fsd.com"), None)      
        self.assertEqual(clean_email(None), None)
        self.assertEqual(clean_email("      "), None)
        self.assertEqual(clean_email("joe smith@gmail.com"), None)
        self.assertEqual(clean_email("joesmith@gm###$#$ail.com"), None)

    def test_clean_phone(self):
        self.assertEqual(clean_phone("   "), None)
        self.assertEqual(clean_phone(None), None)
        self.assertEqual(clean_phone("458) 829-1910"), "4588291910")
        self.assertEqual(clean_phone("111.829-1910"), None)
        self.assertEqual(clean_phone("917.829 - 1910"), "9178291910")
        self.assertEqual(clean_phone("9999999999"), "9999999999")
        self.assertEqual(clean_phone("8"), None)
        self.assertEqual(clean_phone("97.829 - 1910"), None)
        self.assertEqual(clean_phone("+1 297.829 - 1910"), "2978291910")
        self.assertEqual(clean_phone("1297.829 (1910"), "2978291910")
        self.assertEqual(clean_phone("45297.829 (1910"), None)

    def test_valid_fields(self):
        self.assertEqual(contact_9.valid_fields(), ("qq", "qq@gmail.com"))
        self.assertEqual(contact_5.valid_fields(), ("barn", "barn", "barn@gmail.com", "8725922902"))
        self.assertEqual(contact_10.valid_fields(), ())

    def test_score(self):
        self.assertEqual(contact_1.score("query"), 2)
        self.assertEqual(contact_2.score("tina"), 0)
        self.assertEqual(contact_3.score("tin q"), 1)
        self.assertEqual(contact_4.score("qq@gmail.com"), 3)
        self.assertEqual(contact_5.score("barn"), 7)
        self.assertEqual(contact_6.score("b"), 3.2)
        self.assertEqual(contact_7.score("82"), 2)
        self.assertEqual(contact_8.score("82"), 2.1)

    def test_hash(self):
        self.assertNotEqual(hash(contact_10), hash(Contact("a name")))
        self.assertEqual(hash(contact_2), hash(contact_3))
        self.assertNotEqual(hash(contact_6), hash(contact_7))
        # check the __eq__ override as well
        self.assertEqual(contact_10, Contact())
        self.assertNotEqual(contact_12, Contact("one entry", "foo"))

    def test_output_dict(self):
        contact_10_dict = OrderedDict(())
        self.assertEqual(contact_10.output_dict(), contact_10_dict)

        contact_8_dict = OrderedDict([("name","Barn"),("nickname","Barn"),("phone","(827) 259-2282"),("email","barn82@bbmail.com")])
        self.assertEqual(contact_8.output_dict(), contact_8_dict)

        contact_11_dict = OrderedDict([("name","Partial"), ("phone","(800) 999-1000")])
        self.assertEqual(contact_11.output_dict(), contact_11_dict) 

        contact_12_dict = OrderedDict([("name","One Entry")])
        self.assertEqual(contact_12.output_dict(), contact_12_dict)

    def test_sort_contacts(self):
        with open('Testing/empty_contacts.json') as f:
            data1 = list(set([Contact(**j) for j in json.load(f)]))
        self.assertEqual(sort_contacts("any_query", data1), "[]")    
    
        with open('Testing/duplicate_contacts.json') as f:
            data2 = list(set([Contact(**j) for j in json.load(f)]))
        with open('Testing/no_duplicate_contacts.json') as f:
            data3 = list(set([Contact(**j) for j in json.load(f)]))
        self.assertEqual(sort_contacts("Andrew", data2), sort_contacts("Andrew", data3))

        with open('Testing/empty_contacts2.json') as f:
            data4 = list(set([Contact(**j) for j in json.load(f)]))
        self.assertEqual(sort_contacts("whatever", data4), "[]")
        
        with open('Testing/sorted_query_jenny.json') as f:
            data5 = json.load(f)
        # note that this test discards the indent formatting, and the ordering
        # supplied by OrderedDict(). Those two aspects are thus not unit tested.
        self.assertEqual(json.loads(main("jenny")), data5)

if __name__=='__main__':
    unittest.main()
