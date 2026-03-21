import unittest
from pyrenderedterminal import Scene, Actor, Layerer, collides, stamp, rect

class TestPyRenderedTerminal(unittest.TestCase):

    def setUp(self):
        """Initialize a standard scene for testing."""
        self.scene = Scene(width=10, height=5, bg=".")

    ## --- Scene Tests ---
    def test_scene_initialization(self):
        self.assertEqual(self.scene.width, 10)
        self.assertEqual(self.scene.height, 5)
        self.assertEqual(self.scene.get(0, 0), ".")

    def test_draw_and_get(self):
        self.scene.draw(2, 2, "#")
        self.assertEqual(self.scene.get(2, 2), "#")
        self.assertFalse(self.scene.draw(11, 2, "X"))
        self.assertFalse(self.scene.draw(2, 6, "X"))
        self.assertFalse(self.scene.draw(2, 2, "XX"))

    def test_clear_scene(self):
        self.scene.draw(1, 1, "A")
        self.scene.clear()
        self.assertEqual(self.scene.get(1, 1), ".")

    def test_get_out_of_bounds(self):
        self.assertIsNone(self.scene.get(-1, 0))
        self.assertIsNone(self.scene.get(0, 10))

    ## --- Actor Tests ---
    def test_actor_movement(self):
        sprites = {"main": "O"}
        player = Actor(0, 0, sprites)
        player.move(5, 2)
        self.assertEqual(player.x, 5)
        self.assertEqual(player.y, 2)
        
        player.goto(1, 1)
        self.assertEqual(player.x, 1)
        self.assertEqual(player.y, 1)

    def test_actor_clamping(self):
        sprites = {"main": "##\n##"}
        player = Actor(8, 3, sprites)
        player.move(10, 10)
        player.clamp(self.scene)
        self.assertEqual(player.x, 8) 
        self.assertEqual(player.y, 3)
        
    def test_collision_detection(self):
        s1 = {"main": "##\n##"}
        a1 = Actor(0, 0, s1)
        a2 = Actor(1, 1, s1)
        a3 = Actor(5, 5, s1)
        
        self.assertTrue(collides(a1, a2))
        self.assertFalse(collides(a1, a3))

    ## --- Utilities Tests ---
    def test_rect_drawing(self):
        rect(self.scene, 0, 0, 2, 2, "R")
        self.assertEqual(self.scene.get(0, 0), "R")
        self.assertEqual(self.scene.get(1, 1), "R")
        self.assertEqual(self.scene.get(2, 2), ".")

    def test_layering_logic(self):
        layerer = Layerer(10, 5, bg=".")
        scene1 = Scene(10, 5, bg=".")
        scene2 = Scene(10, 5, bg=".")
        
        scene1.draw(0, 0, "1")
        scene2.draw(0, 0, "2")
        
        layerer.add_layer(scene1)
        layerer.add_layer(scene2)
        
        layerer.update()
        self.assertIn("2", layerer.scenestr.split("\n")[0])
    
    def test_layer_size_mismatch(self):
        layerer = Layerer(10, 5)
        bad_scene = Scene(5, 5)
        
        layerer.add_layer(bad_scene)
        self.assertEqual(len(layerer.layers), 0)

    def test_stamp(self):
        sprite = "AB\nCD"
        stamp(self.scene, 0, 0, sprite)
        
        self.assertEqual(self.scene.get(0, 0), "A")
        self.assertEqual(self.scene.get(1, 0), "B")
        self.assertEqual(self.scene.get(0, 1), "C")
        self.assertEqual(self.scene.get(1, 1), "D")

if __name__ == "__main__":
    unittest.main()
