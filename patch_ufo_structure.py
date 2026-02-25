with open('viewer3d/components/ImmersiveScene.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Fix UFO button text - main button
old1 = '                \U0001f6f8 UFO {currentUfo}\n              </button>'
new1 = '                \u00f0\u0178\u008c\n              </button>'
if old1 in content:
    content = content.replace(old1, new1, 1)
    changes += 1
    print('Step 1 OK: main UFO button fixed')
else:
    # Try with the actual emoji
    old1b = '                \U0001f6f8 UFO {currentUfo}'
    if old1b in content:
        idx = content.index(old1b)
        print(f'Found at {idx}:', repr(content[idx:idx+50]))
    print('Step 1 FAIL')

# 2. Fix UFO dropdown items text
old2 = '                      \U0001f6f8 UFO {ufoNum}\n                    </button>'
new2 = '                      \u00f0\u0178\u008c\n                    </button>'
if old2 in content:
    content = content.replace(old2, new2)
    changes += 1
    print('Step 2 OK: dropdown UFO buttons fixed')
else:
    print('Step 2 FAIL')

# Also fix justifyContent center on main button
old3 = "                  display: 'flex',\n                  alignItems: 'center',\n                  gap: '8px',\n                  transition: 'all 0.2s',\n                  boxShadow: '0 4px 12px rgba(0,0,0,0.3)',\n                  width: '100%'"
new3 = "                  display: 'flex',\n                  alignItems: 'center',\n                  justifyContent: 'center',\n                  gap: '8px',\n                  transition: 'all 0.2s',\n                  boxShadow: '0 4px 12px rgba(0,0,0,0.3)',\n                  width: '100%'"
if old3 in content:
    content = content.replace(old3, new3, 1)
    changes += 1
    print('Step 3 OK: justifyContent center added')
else:
    print('Step 3 SKIP: already has it or not found')

print(f'Total changes: {changes}')

with open('viewer3d/components/ImmersiveScene.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
