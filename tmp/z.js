// ============================================================
//  Velária MMORPG — ZONAS DE TIER (1.1.29)
//  O mapa é dividido em anéis a partir do centro (os mesmos raios da parede de tier):
//    até 1500 = zona 1, até 3000 = zona 2, até 5000 = zona 3, até 8000 = zona 4, além = zona 5.
//  Chefes e mobs de mods têm um tier. Eles só podem existir quando:
//    1) o tier deles cabe na zona onde estão (Frostmaw T2 não aparece na zona 1), e
//    2) o admin já liberou aquele tier no servidor:  /zona liberar <1-5>
//  Vale para spawn natural E para entidades salvas no chunk (as que já existiam somem ao carregar).
//  Ovos, /summon e spawns de admin passam se o comando for usado por op (tag velaria_admin_spawn).
//  /zona status mostra o tier liberado. Também no /painel.
// ============================================================
const VZ = {
  centro: { x: 0, z: 0 },
  aneis: [1500, 3000, 5000, 8000],
  // tier padrão por mod (mobs comuns do mod) — chefes têm tier próprio em VG.VELARIA_CHEFES
  porMod: {
    mowziesmobs: 2, iceandfire: 3, bosses_of_mass_destruction: 3, cataclysm: 4,
    born_in_chaos_v1: 2, aquamirae: 3, deeperdarker: 4
  },
  // mobs desses mods que são "comuns" e ficam livres no tier 1
  livres: /^mowziesmobs:(foliaath|baby_foliaath|lantern|naga|grottol|bluff)$/,
  chefes: {
    'mowziesmobs:ferrous_wroughtnaut': 2, 'mowziesmobs:frostmaw': 2, 'minecraft:elder_guardian': 2,
    'bosses_of_mass_destruction:lich': 3, 'bosses_of_mass_destruction:void_blossom': 3,
    'mowziesmobs:umvuthi': 3, 'mowziesmobs:sculptor': 3,
    'bosses_of_mass_destruction:gauntlet': 4, 'bosses_of_mass_destruction:obsidilith': 4,
    'minecraft:wither': 4, 'cataclysm:ignis': 4, 'cataclysm:netherite_monstrosity': 4, 'minecraft:warden': 4
  }
}

function vzZona(x, z) {
  let d = Math.sqrt((x - VZ.centro.x) * (x - VZ.centro.x) + (z - VZ.centro.z) * (z - VZ.centro.z))
  for (let i = 0; i < VZ.aneis.length; i++) if (d <= VZ.aneis[i]) return i + 1
  return 5
}
function vzTierEntidade(id) {
  if (VZ.chefes[id]) return VZ.chefes[id]
  if (VZ.livres.test(id)) return 0
  let ns = id.substring(0, id.indexOf(':'))
  return VZ.porMod[ns] || 0
}
function vzLiberado(server) {
  let t = server.persistentData.getInt('velaria_zona_liberada')
  return t > 0 ? t : 1
}
VG.velariaZona = vzZona
VG.velariaZonaLiberada = vzLiberado

EntityEvents.spawned(event => {
  let e = event.entity
  if (!e || e.isPlayer()) return
  try {
    if (String(e.level.dimension) !== 'minecraft:overworld') return
    let t = vzTierEntidade(String(e.type))
    if (t <= 1) return
    if (e.tags.contains('velaria_admin_spawn')) return
    if (t <= vzZona(e.x, e.z) && t <= vzLiberado(e.server)) return
    event.cancel()
  } catch (err) { }
})

ServerEvents.commandRegistry(event => {
  let { commands: Commands, arguments: Arguments } = event
  event.register(Commands.literal('zona').requires(s => s.hasPermission(2))
    .then(Commands.literal('status').executes(ctx => {
      let s = ctx.source.server
      ctx.source.sendSystemMessage(Text.gold(`Tier liberado no mundo: ${vzLiberado(s)} · anéis ${VZ.aneis.join(' / ')} blocos`))
      return 1
    }))
    .then(Commands.literal('liberar').then(Commands.argument('n', Arguments.INTEGER.create(event)).executes(ctx => {
      let n = Math.max(1, Math.min(5, Arguments.INTEGER.getResult(ctx, 'n')))
      let s = ctx.source.server
      s.persistentData.putInt('velaria_zona_liberada', n)
      s.tell(Text.gold(`[Velária] Criaturas de tier até ${n} liberadas nas suas zonas.`))
      return 1
    }))))
})

// Varredura: entidades que entraram sem passar pelo evento (spawn chunks, estruturas) — a cada 5 s
ServerEvents.tick(ev => {
  if (ev.server.tickCount % 100 !== 0) return
  try {
    let lv = ev.server.overworld()
    let lib = vzLiberado(ev.server)
    lv.getEntities().forEach(e => {
      if (e.isPlayer()) return
      let t = vzTierEntidade(String(e.type))
      if (t <= 1 || e.tags.contains('velaria_admin_spawn')) return
      if (t <= vzZona(e.x, e.z) && t <= lib) return
      e.discard()
    })
  } catch (err) { }
})
