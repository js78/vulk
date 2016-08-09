import OpenGL.GL as gl
import OpenGL.GL.shaders as gl_shaders


class ShaderProgram():
    def __init__(self, vertex, fragment, geometry=None, compute=None,
                 tesselation_evaluation=None, tesselation_control=None):
        shaders = []

        def add_shader(shader, gl_shader):
            shaders.append(gl_shaders.compileShader(shader, gl_shader))

        add_shader(vertex, gl.GL_VERTEX_SHADER)
        add_shader(fragment, gl.GL_FRAGMENT_SHADER)

        optionals = {
            gl.GL_GEOMETRY_SHADER: geometry,
            gl.GL_COMPUTE_SHADER: compute,
            gl.GL_TESS_CONTROL_SHADER: tesselation_control,
            gl.GL_TESS_EVALUATION_SHADER: tesselation_evaluation}

        for key, value in optionals.items():
            if value:
                add_shader(value, key)

        self._shaders = shaders
        self.handle = gl_shaders.compileProgram(*self._shaders)

    def __enter__(self):
        gl.glUseProgram(self.handle)
        return self

    def __exit__(self, *args):
        gl.glUseProgram(0)

    def delete(self):
        gl.glUseProgram(0)

        for shader in self._shaders:
            gl.glDeleteShader(shader)

        gl.glDeleteProgram(self.handle)

        self._shaders = None
        self.handle = None
