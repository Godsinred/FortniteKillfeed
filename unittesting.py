import unittesting
import FortniteTracker
import Main as m


class FortniteTest(unittesting.TestCase):
    """
    unittesting class for the fortnite app
    """
    def setUp(self):
        """
        sets up the header to be the appropriate api key and creates a fortnite tracker object
        :return:
        """
        self.header = {'TRN-Api-Key': "fbb96ada-6ac7-4e7d-b1eb-1d0b32011d54"}
        self.fortnite_database = FortniteTracker.FortniteTracker(self.header['TRN-Api-Key'])

    def test_add_player(self):
        """
        tests the adding the new player into the sql database and checks if the data in sql is correct.
        :param: none
        :return: none
        """
        self.fortnite_database.add_player("Dark")
        cmd = """SELECT * FROM Players WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark")])

        self.fortnite_database.add_player("Ninja")
        cmd = """SELECT * FROM Players WHERE username='Ninja'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Ninja")])

        self.fortnite_database.add_player("cupidie")
        cmd = """SELECT * FROM Players WHERE username='cupidie'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(3, "cupidie")])

        self.fortnite_database.add_player("manduin wyrnn")
        cmd = """SELECT * FROM Players WHERE username='manduin wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(4, "manduin wyrnn")])

        self.fortnite_database.add_player("sbib")
        cmd = """SELECT * FROM Players WHERE username='sbib'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(5, "sbib")])

    def test_add_weapon_stats(self):
        """
        test_add_weapon_stats tests if weapon is correctly adding it when a new player is being added into the database.
        It checks if the added weapon for existing player is correctly added.
        :param: none
        :return: none
        """
        self.fortnite_database.add_player("Dark")
        self.fortnite_database.add_weapon_stats("Dark")
        cmd = """SELECT * FROM WeaponStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark", 0, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("Ninja")
        self.fortnite_database.add_weapon_stats("Ninja")
        cmd = """SELECT * FROM WeaponStats WHERE username='Ninja'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Ninja", 0, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("cupidie")
        self.fortnite_database.add_weapon_stats("cupidie")
        cmd = """SELECT * FROM WeaponStats WHERE username='cupidie'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(3, "cupidie", 0, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("manduin wyrnn")
        self.fortnite_database.add_weapon_stats("manduin wyrnn")
        cmd = """SELECT * FROM WeaponStats WHERE username='manduin wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(4, "manduin wyrnn", 0, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("sbib")
        self.fortnite_database.add_weapon_stats("sbib")
        cmd = """SELECT * FROM WeaponStats WHERE username='sbib'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(5, "sbib", 0, 0, 0, 0, 0, 0)])

    def test_update_weapon_stats(self):
        """
        test_update_weapon_stats checks if the weapon of the eixisting player updates correctly.
        Add player by using add_player fucntion, and updates his weapon stats with update_weapon_stats
        function. Lastly, we compare it with the expected data.
        :param: none
        :return: none
        """
        self.fortnite_database.add_player("Dark")
        self.fortnite_database.add_weapon_stats("Dark")
        self.fortnite_database.update_weapon_stats("Dark", "shotgun")
        cmd = """SELECT * FROM WeaponStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(1, "Dark", 1, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("Ninja")
        self.fortnite_database.add_weapon_stats("Ninja")
        self.fortnite_database.update_weapon_stats("Ninja", "pistol")
        cmd = """SELECT * FROM WeaponStats WHERE username='Ninja'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Ninja", 0, 1, 0, 0, 0, 0)])

        self.fortnite_database.add_player("cupidie")
        self.fortnite_database.add_weapon_stats("cupidie")
        self.fortnite_database.update_weapon_stats("cupidie", "shotgun")
        cmd = """SELECT * FROM WeaponStats WHERE username='cupidie'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(3, "cupidie", 1, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("manduin wyrnn")
        self.fortnite_database.add_weapon_stats("manduin wyrnn")
        self.fortnite_database.update_weapon_stats("manduin wyrnn", "shotgun")
        cmd = """SELECT * FROM WeaponStats WHERE username='manduin wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(4, "manduin wyrnn", 1, 0, 0, 0, 0, 0)])

        self.fortnite_database.add_player("sbib")
        self.fortnite_database.add_weapon_stats("sbib")
        self.fortnite_database.update_weapon_stats("sbib", "shotgun")
        cmd = """SELECT * FROM WeaponStats WHERE username='sbib'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(5, "sbib", 1, 0, 0, 0, 0, 0)])

    def test_update_db(self):
        """
        test_update_db checks if the weapon of the eixisting player updates correctly.
        We use the function update_db in fortnite_database class, and passes the expected result.
         hich should update the killer, they way he died, who is dead and the possible weapon.
        :param: none
        :return: none
        """
        self.fortnite_database.update_db("Manduin Wyrnn bludgeoned Cupidie", "bludgeoned", "pickaxe")
        cmd = """SELECT * FROM CurrentStats WHERE username='Manduin Wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Manduin Wyrnn", "N/A", 1, "pickaxe", 0, 0, 0, 0, 0, 1)])

        self.fortnite_database.update_db("sphaerophoria shotgunned Stein72", "shotgunned", "shotgun")
        cmd = """SELECT * FROM CurrentStats WHERE username='sphaerophoria'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(4, "sphaerophoria", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        self.fortnite_database.update_db("cupidie shotgunned Stein", "shotgunned", "shotgun")
        cmd = """SELECT * FROM CurrentStats WHERE username='cupidie'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(6, "cupidie", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        self.fortnite_database.update_db("Dark shotgunned manduin", "shotgunned", "shotgun")
        cmd = """SELECT * FROM CurrentStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(8, "Dark", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        self.fortnite_database.update_db("Ninja shotgunned sbib", "shotgunned", "shotgun")
        cmd = """SELECT * FROM CurrentStats WHERE username='Ninja'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(10, "Ninja", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

    def test_process_text(self):
        """
        test_process_text checks if the correct user name was picked up.
        :param: none
        :return: none
        """
        m.process_text("Manduin Wyrnn bludgeoned Cupidie", self.fortnite_database)
        cmd = """SELECT * FROM CurrentStats WHERE username='Manduin Wyrnn'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(2, "Manduin Wyrnn", "N/A", 1, "pickaxe", 0, 0, 0, 0, 0, 1)])

        m.process_text("sphaerophoria shotgunned Stein72", self.fortnite_database)
        cmd = """SELECT * FROM CurrentStats WHERE username='sphaerophoria'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(4, "sphaerophoria", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        m.process_text("cupidie shotgunned Stein", self.fortnite_database)
        cmd = """SELECT * FROM CurrentStats WHERE username='cupidie'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(6, "cupidie", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        m.process_text("Dark shotgunned manduin", self.fortnite_database)
        cmd = """SELECT * FROM CurrentStats WHERE username='Dark'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(8, "Dark", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

        m.process_text("Ninja shotgunned sbib", self.fortnite_database)
        cmd = """SELECT * FROM CurrentStats WHERE username='Ninja'"""
        self.fortnite_database.cur.execute(cmd)
        result = self.fortnite_database.cur.fetchall()
        self.assertEqual(result, [(10, "Ninja", "N/A", 1, "shotgun", 0, 0, 0, 0, 0, 1)])

    def test_update_sentence(self):
        """
        test_process_text checks if the sentence is updated correctly by using similarity percentage.
        Compares it with the expected result.
        :param: none
        :return: none
        """
        result = m.update_sentence("Manduin Wyrnn bludgeomed Cupidie")
        self.assertMultiLineEqual(result, "Manduin Wyrnn bludgeoned Cupidie")

        result = m.update_sentence("sphaerophoria shotaunned Stein72")
        self.assertMultiLineEqual(result, "sphaerophoria shotgunned Stein72")

        result = m.update_sentence("Manduin Wyrnn chedked out early")
        self.assertMultiLineEqual(result, "Manduin Wyrnn checked out early")

        result = m.update_sentence("Manduin Wyrnn was l0st in the storm")
        self.assertMultiLineEqual(result, "Manduin Wyrnn was lost in the storm")

        result = m.update_sentence("Manduin Wyrnn is literaily on fire")
        self.assertMultiLineEqual(result, "Manduin Wyrnn is literally on fire")


if __name__ == "__main__":
    unittesting.main()