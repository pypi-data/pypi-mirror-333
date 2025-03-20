import asyncio
import sys
import os
from typing import Dict, Any, List

# Ajustamos la ruta para encontrar el módulo server en src/mcp_build_toolchain
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.append(src_path)

# Importamos el servidor desde el módulo correcto
from mcp_build_toolchain.server import server

async def test_list_tools():
    """Prueba la funcionalidad de listar herramientas disponibles"""
    print("=== Probando handle_list_tools() ===")
    try:
        # Llamamos directamente a la función handle_list_tools definida en el servidor
        from mcp_build_toolchain.server import handle_list_tools
        tools = await handle_list_tools()
        print(f"Herramientas disponibles: {len(tools)}")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print(f"  Schema de entrada: {tool.inputSchema}")
        return tools
    except Exception as e:
        print(f"Error al listar herramientas: {e}")
        return []

async def test_get_compilation_errors(outfile: str):
    """Prueba la herramienta get-compilation-errors"""
    print(f"\n=== Probando get-compilation-errors con archivo: {outfile} ===")
    try:
        # Llamamos directamente a la función handle_call_tool definida en el servidor
        from mcp_build_toolchain.server import handle_call_tool
        result = await handle_call_tool(
            name="get-compilation-errors",
            arguments={"outfile": outfile}
        )
        print("Errores y advertencias encontrados:")
        for content in result:
            if hasattr(content, "text"):
                print(content.text)
        return result
    except Exception as e:
        print(f"Error al obtener errores de compilación: {e}")
        return None

async def test_get_compilation_errors_with_regexp(outfile: str, regexp: str):
    """Prueba la herramienta get-compilation-errors con parámetro regexp personalizado"""
    print(f"\n=== Probando get-compilation-errors con archivo: {outfile} y regexp: {regexp} ===")
    try:
        # Llamamos directamente a la función handle_call_tool definida en el servidor
        from mcp_build_toolchain.server import handle_call_tool
        result = await handle_call_tool(
            name="get-compilation-errors",
            arguments={"outfile": outfile, "regexp": regexp}
        )
        print("Errores y advertencias filtrados por regexp personalizado:")
        for content in result:
            if hasattr(content, "text"):
                print(content.text)
        return result
    except Exception as e:
        print(f"Error al obtener errores de compilación con regexp: {e}")
        return None

async def run_complete_test():
    """Ejecuta todas las pruebas en secuencia"""
    # 1. Listar herramientas disponibles
    tools = await test_list_tools()
    
    if not tools:
        print("No se pudieron obtener las herramientas. Finalizando pruebas.")
        return
    
    # test_outfile = 'test_outfile.txt'
    # with open(test_outfile, "w") as f:
    #     f.write("gcc: warning: ignoring nonexistent directory\n")
    #     f.write("main.c:10:15: error: 'foo' undeclared\n")
    #     f.write("This is a normal line\n")
    #     f.write("main.c:20:5: Warning: unused variable 'x'\n")
    #     f.write("main.c:Error #20 Warning: unused variable 'x'\n")
    #     f.write("Test adding not ansi character. ó à ü\n")

    test_outfile = 'E:\Projects\GRFID\minicoms-code\sw-code-mini\source\out\TMS570.log'
    
    # 4. Obtener errores de compilación con el regexp por defecto
    errors_result = await test_get_compilation_errors(test_outfile)
    
    # 5. Obtener errores de compilación con un regexp personalizado
    # Usamos un regexp que solo captura líneas con 'main.c'
    #custom_regexp = r'main\.c'
    custom_regexp = 'error #|warning #'
    custom_errors_result = await test_get_compilation_errors_with_regexp(test_outfile, custom_regexp)
    
    # 6. Limpiar archivo temporal
    try:
        # os.remove(test_outfile)
        print(f"\nArchivo temporal {test_outfile} eliminado.")
    except:
        print(f"\nNo se pudo eliminar el archivo temporal {test_outfile}.")

    print("\n=== Pruebas completadas ===")

if __name__ == "__main__":
    # Ejecutar todas las pruebas
    asyncio.run(run_complete_test())
