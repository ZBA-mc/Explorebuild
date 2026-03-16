import pyglet
from pyglet.window import key, mouse
import pyglet.gl as gl
from perlin_noise import PerlinNoise
import numpy as np
import random
import math

WINDOW_SIZE = (900, 600)
BLOCK_SIZE = 1.0
CHUNK_SIZE = 32
BLOCK_TYPES = [
    {"name": "grass", "color": (0.4, 1.0, 0.4)},   # RGB
    {"name": "stone", "color": (0.6, 0.6, 0.6)},
    {"name": "dirt", "color": (0.7, 0.5, 0.3)},
    {"name": "bedrock", "color": (0.25, 0.25, 0.25)},
]

class Camera:
    def __init__(self, pos, pitch=0.0, yaw=0.0):
        self.pos = np.array(pos, dtype="float32")
        self.pitch = pitch
        self.yaw = yaw
        self.speed = 0.08
        self.sensitivity = 0.2

    def get_direction(self):
        pitch_rad = math.radians(self.pitch)
        yaw_rad = math.radians(self.yaw)
        x = -math.sin(yaw_rad) * math.cos(pitch_rad)
        y = math.sin(pitch_rad)
        z = -math.cos(yaw_rad) * math.cos(pitch_rad)
        return np.array([x, y, z], dtype="float32")

class BlockWorld:
    def __init__(self):
        self.blocks = {}  # (x,y,z) -> {"type": int}
        self.noise = PerlinNoise(octaves=4, seed=int(random.uniform(0,10000)))
        self.generate_chunk()

    def generate_chunk(self):
        for z in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                y = int(self.noise([x/24, z/24]) * 8)
                self.blocks[(x, y, z)] = {"type": 0}  # grass
                for d in range(-2, y):
                    self.blocks[(x, d, z)] = {"type": 2}  # dirt

    def get_block_at(self, pos):
        return self.blocks.get(tuple(pos))

    def add_block(self, pos, block_type):
        self.blocks[tuple(pos)] = {"type": block_type}

    def remove_block(self, pos):
        self.blocks.pop(tuple(pos), None)

    def blocks_in_frustum(self, cam_pos, max_dist=40):
        # Simple distance filter, no true frustum
        return [
            (pos, info["type"])
            for pos, info in self.blocks.items()
            if np.linalg.norm(np.array(pos) - cam_pos) < max_dist
        ]

class PauseMenu:
    def __init__(self):
        self.visible = False
        self.label = pyglet.text.Label(
            "Pause Menu\n[Esc] Continue | [Q] Quit",
            font_size=28,
            color=(255,255,255,255),
            x=WINDOW_SIZE[0]//2, y=WINDOW_SIZE[1]//2,
            anchor_x="center", anchor_y="center"
        )
    def draw(self):
        if self.visible:
            gl.glDisable(gl.GL_DEPTH_TEST)
            self.label.draw()
            gl.glEnable(gl.GL_DEPTH_TEST)

class Player:
    def __init__(self, spawn=(8, 10, 8)):
        self.cam = Camera(list(spawn), pitch=0.0, yaw=0.0)
        self.velocity = np.array([0,0,0],dtype="float32")
        self.on_ground = False
    def move(self, direction, dt):
        self.cam.pos += direction * self.cam.speed * dt

# --------- OpenGL helpers ------------
def draw_cube(x, y, z, block_type):
    color = BLOCK_TYPES[block_type]["color"]
    vertices = [
        # Front
        x+0, y+0, z+1,  x+1, y+0, z+1,  x+1, y+1, z+1,  x+0, y+1, z+1,
        # Back
        x+0, y+0, z+0,  x+1, y+0, z+0,  x+1, y+1, z+0,  x+0, y+1, z+0,
    ]
    faces = [
        (0,1,2,3), # Front
        (4,5,6,7), # Back
        (3,2,6,7), # Top
        (0,1,5,4), # Bottom
        (1,2,6,5), # Right
        (0,3,7,4), # Left
    ]
    verts = []
    for face in faces:
        for idx in face:
            verts.extend(vertices[idx*3:idx*3+3])
    pyglet.graphics.draw(len(verts)//3, gl.GL_QUADS,
        ('v3f/static', verts),
        ('c3f/static', color * (len(verts)//3))
    )

# --------- Main App ------------
class ExploreBuildApp(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], caption="Explorebuild Pyglet2 3D", resizable=True)
        self.set_exclusive_mouse(True)  # 捕获鼠标
        self.world = BlockWorld()
        self.player = Player()
        self.pause_menu = PauseMenu()
        self.block_pick = 0  # 当前选中的方块类型
        self.coord_label = pyglet.text.Label("", x=10, y=self.height-30, font_size=14, batch=None)
        self.show_coords = False
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.keys = set()
        self.paused = False

    def on_draw(self):
        self.clear()
        gl.glEnable(gl.GL_DEPTH_TEST)
        self.setup_3d()
        cam = self.player.cam
        # 坐标与视角
        gl.glLoadIdentity()
        gl.gluLookAt(
            cam.pos[0], cam.pos[1], cam.pos[2],
            cam.pos[0]+cam.get_direction()[0], cam.pos[1]+cam.get_direction()[1], cam.pos[2]+cam.get_direction()[2],
            0, 1, 0
        )
        # 绘制方块
        for (pos, typ) in self.world.blocks_in_frustum(cam.pos):
            draw_cube(*pos, typ)
        gl.glDisable(gl.GL_DEPTH_TEST)
        if self.show_coords:
            self.coord_label.text = f"X:{cam.pos[0]:.2f} Y:{cam.pos[1]:.2f} Z:{cam.pos[2]:.2f}"
            self.coord_label.draw()
        self.fps_display.draw()
        self.pause_menu.draw()

    def setup_3d(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.gluPerspective(70, self.width/self.height, 0.1, 1000)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.paused: return
        self.player.cam.yaw += dx * self.player.cam.sensitivity
        self.player.cam.pitch -= dy * self.player.cam.sensitivity
        self.player.cam.pitch = max(-89, min(89, self.player.cam.pitch))

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.paused = not self.paused
            self.pause_menu.visible = self.paused
            self.set_exclusive_mouse(not self.paused)
        if self.paused:
            if symbol == key.Q:  # quit
                self.close()
            if symbol == key.ESCAPE:
                self.paused = False
                self.pause_menu.visible = False
                self.set_exclusive_mouse(True)
            return
        # 方块切换
        if symbol in (key._1, key._2, key._3, key._4):
            self.block_pick = symbol - key._1
        if symbol == key.F3:
            self.show_coords = not self.show_coords
        # 可添加更多快捷键

    def on_mouse_press(self, x, y, button, modifiers):
        if self.paused: return
        # 射线检测: 获取玩家视角方向前方最靠近的方块
        cam = self.player.cam
        cam_pos = np.copy(cam.pos)
        look_dir = cam.get_direction()
        for step in np.linspace(0, 12, 50):
            probe = cam_pos + look_dir * step
            hit = self.world.get_block_at(tuple(map(int, probe)))
            if hit:
                if button == mouse.RIGHT:
                    self.world.remove_block(tuple(map(int, probe)))
                elif button == mouse.LEFT:
                    # 在碰撞面前再生一个方块
                    face_pos = tuple(map(int, probe + look_dir * 0.5))
                    self.world.add_block(face_pos, self.block_pick)
                break

    def on_text_motion(self, motion):
        # 空格跳跃
        if motion == key.MOTION_UP and self.player.on_ground:
            self.player.velocity[1] = 0.16

    def update(self, dt):
        if self.paused: return
        cam = self.player.cam
        move_dir = np.array([0,0,0],dtype="float32")
        if key.W in self.keys:
            move_dir += cam.get_direction()
        if key.S in self.keys:
            move_dir -= cam.get_direction()
        if key.A in self.keys:
            # 左向
            left = np.cross(cam.get_direction(), [0,1,0])
            move_dir += left
        if key.D in self.keys:
            # 右向
            right = np.cross([0,1,0], cam.get_direction())
            move_dir += right
        if key.SPACE in self.keys:
            if self.player.on_ground:
                self.player.velocity[1] = 0.16
        # 更新位置
        self.player.move(move_dir, dt)
        # 跳跃&重力
        self.player.cam.pos[1] += self.player.velocity[1]
        self.player.velocity[1] -= 0.008
        if self.player.cam.pos[1] <= 5:
            self.player.cam.pos[1] = 5
            self.player.velocity[1] = 0
            self.player.on_ground = True
        else:
            self.player.on_ground = False

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.W, key.A, key.S, key.D, key.SPACE):
            self.keys.discard(symbol)

    def on_key_press_continuous(self, symbol, modifiers):
        if symbol in (key.W, key.A, key.S, key.D, key.SPACE):
            self.keys.add(symbol)

    def on_resize(self, width, height):
        self.coord_label.y = height - 30

def main():
    app = ExploreBuildApp()
    pyglet.clock.schedule_interval(app.update, 1/60)
    # 持续检测按键持有
    @app.event
    def on_key_press(symbol, modifiers):
        app.on_key_press_continuous(symbol, modifiers)
        app.on_key_press(symbol, modifiers)
    @app.event
    def on_key_release(symbol, modifiers):
        app.on_key_release(symbol, modifiers)
    app.run()

if __name__ == "__main__":
    main()
