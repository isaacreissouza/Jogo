# teste_player.py
import player
import inspect

print("player.__file__:", getattr(player, '__file__', 'NÃO ENCONTRADO'))
Player = getattr(player, 'Player', None)
print("Player repr:", Player)
print("has single_fire_event in class?:", hasattr(Player, 'single_fire_event'))
try:
    print("inspect.signature(Player.single_fire_event):", inspect.signature(Player.single_fire_event))
except Exception as e:
    print("inspect.signature erro:", e)

# cria instância (passa um objeto simples como 'game' para não precisar do jogo inteiro)
class DummyGame: pass
if Player:
    inst = Player(DummyGame())
    print("inst has single_fire_event?:", hasattr(inst, 'single_fire_event'))
    print("dir(inst) preview:", [n for n in dir(inst) if 'single' in n or 'fire' in n])
