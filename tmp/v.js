// ============================================================
//  Velária MMORPG — EFEITOS DE ATAQUE (1.1.19)
//  Pasta: kubejs/server_scripts/  (recarrega com /reload)  GERADO por tools/gen_vfx.py
//  - Armas do kit: cada golpe que acerta desenha o rastro do golpe no ar (arco largo da espada longa,
//    corte duplo da katana, estocada da lança, onda de choque do martelo e do machado duplo...).
//    Tier 1-2: rastro simples. Tier 3+: com a partícula do material (fogo da Vulcanita, gelo da
//    Glaciarita, faíscas da Tempestita...). Tier 4-5: explosão de energia no alvo.
//  - Arcos e bestas (qualquer mod): a flecha deixa rastro conforme o tier do jogador e estoura no alvo.
//  As partículas são enviadas pelo servidor para todos que estão perto.
// ============================================================

const VFX = { armas: {"kubejs:estanho_claymore": ["claymore", 1, "minecraft:crit", "minecraft:crit"], "kubejs:estanho_katana": ["katana", 1, "minecraft:crit", "minecraft:crit"], "kubejs:estanho_sword": ["sword", 1, "minecraft:crit", "minecraft:crit"], "kubejs:bronze_solar_hammer": ["hammer", 1, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:bronze_solar_sword": ["sword", 1, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:bronze_solar_spear": ["spear", 1, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:ferro_brasa_double_axe": ["double_axe", 1, "minecraft:flame", "minecraft:lava"], "kubejs:ferro_brasa_hammer": ["hammer", 1, "minecraft:flame", "minecraft:lava"], "kubejs:ferro_brasa_claymore": ["claymore", 1, "minecraft:flame", "minecraft:lava"], "kubejs:ambar_dagger": ["dagger", 1, "minecraft:smoke", "minecraft:smoke"], "kubejs:ambar_sword": ["sword", 1, "minecraft:smoke", "minecraft:smoke"], "kubejs:verdecobre_spear": ["spear", 1, "minecraft:cloud", "minecraft:cloud"], "kubejs:prata_lupina_sword": ["sword", 1, "minecraft:enchant", "minecraft:enchant"], "kubejs:jade_monastico_knuckle": ["knuckle", 1, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:jade_monastico_spear": ["spear", 1, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:jade_monastico_katana": ["katana", 1, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:ambar_crepuscular_katana": ["katana", 1, "minecraft:witch", "minecraft:witch"], "kubejs:ambar_crepuscular_claymore": ["claymore", 1, "minecraft:witch", "minecraft:witch"], "kubejs:prata_hammer": ["hammer", 1, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:prata_spear": ["spear", 1, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:malaquita_scythe": ["scythe", 1, "minecraft:composter", "minecraft:composter"], "kubejs:malaquita_spear": ["spear", 1, "minecraft:composter", "minecraft:composter"], "kubejs:oricalco_claymore": ["claymore", 2, "minecraft:crit", "minecraft:crit"], "kubejs:oricalco_katana": ["katana", 2, "minecraft:crit", "minecraft:crit"], "kubejs:oricalco_sword": ["sword", 2, "minecraft:crit", "minecraft:crit"], "kubejs:cobalto_hammer": ["hammer", 2, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:cobalto_sword": ["sword", 2, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:cobalto_spear": ["spear", 2, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:ferro_sombrio_double_axe": ["double_axe", 2, "minecraft:lava", "minecraft:lava"], "kubejs:ferro_sombrio_hammer": ["hammer", 2, "minecraft:lava", "minecraft:lava"], "kubejs:ferro_sombrio_claymore": ["claymore", 2, "minecraft:lava", "minecraft:lava"], "kubejs:sombraco_dagger": ["dagger", 2, "minecraft:smoke", "minecraft:smoke"], "kubejs:sombraco_sword": ["sword", 2, "minecraft:smoke", "minecraft:smoke"], "kubejs:mitril_spear": ["spear", 2, "minecraft:cloud", "minecraft:cloud"], "kubejs:glaciarita_sword": ["sword", 2, "minecraft:snowflake", "minecraft:enchant"], "kubejs:onix_knuckle": ["knuckle", 2, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:onix_spear": ["spear", 2, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:onix_katana": ["katana", 2, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:onix_crepuscular_katana": ["katana", 2, "minecraft:witch", "minecraft:witch"], "kubejs:onix_crepuscular_claymore": ["claymore", 2, "minecraft:witch", "minecraft:witch"], "kubejs:argentea_celeste_hammer": ["hammer", 2, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:argentea_celeste_spear": ["spear", 2, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:bronze_verdejante_scythe": ["scythe", 2, "minecraft:composter", "minecraft:composter"], "kubejs:bronze_verdejante_spear": ["spear", 2, "minecraft:composter", "minecraft:composter"], "kubejs:aco_legionario_claymore": ["claymore", 3, "minecraft:crit", "minecraft:crit"], "kubejs:aco_legionario_katana": ["katana", 3, "minecraft:crit", "minecraft:crit"], "kubejs:aco_legionario_sword": ["sword", 3, "minecraft:crit", "minecraft:crit"], "kubejs:aco_auroral_hammer": ["hammer", 3, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:aco_auroral_sword": ["sword", 3, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:aco_auroral_spear": ["spear", 3, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:vulcanita_double_axe": ["double_axe", 3, "minecraft:flame", "minecraft:lava"], "kubejs:vulcanita_hammer": ["hammer", 3, "minecraft:flame", "minecraft:lava"], "kubejs:vulcanita_claymore": ["claymore", 3, "minecraft:flame", "minecraft:lava"], "kubejs:sangue_velado_dagger": ["dagger", 3, "minecraft:smoke", "minecraft:smoke"], "kubejs:sangue_velado_sword": ["sword", 3, "minecraft:smoke", "minecraft:smoke"], "kubejs:tempestita_spear": ["spear", 3, "minecraft:electric_spark", "minecraft:cloud"], "kubejs:abissita_sword": ["sword", 3, "minecraft:sculk_soul", "minecraft:enchant"], "kubejs:trovejade_knuckle": ["knuckle", 3, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:trovejade_spear": ["spear", 3, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:trovejade_katana": ["katana", 3, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:sangrita_katana": ["katana", 3, "minecraft:crimson_spore", "minecraft:witch"], "kubejs:sangrita_claymore": ["claymore", 3, "minecraft:crimson_spore", "minecraft:witch"], "kubejs:animita_hammer": ["hammer", 3, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:animita_spear": ["spear", 3, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:ferrocerne_scythe": ["scythe", 3, "minecraft:composter", "minecraft:composter"], "kubejs:ferrocerne_spear": ["spear", 3, "minecraft:composter", "minecraft:composter"], "kubejs:escama_legionaria_claymore": ["claymore", 4, "minecraft:crit", "minecraft:crit"], "kubejs:escama_legionaria_katana": ["katana", 4, "minecraft:crit", "minecraft:crit"], "kubejs:escama_legionaria_sword": ["sword", 4, "minecraft:crit", "minecraft:crit"], "kubejs:escama_aurea_hammer": ["hammer", 4, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:escama_aurea_sword": ["sword", 4, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:escama_aurea_spear": ["spear", 4, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:sangue_dragao_double_axe": ["double_axe", 4, "minecraft:lava", "minecraft:lava"], "kubejs:sangue_dragao_hammer": ["hammer", 4, "minecraft:lava", "minecraft:lava"], "kubejs:sangue_dragao_claymore": ["claymore", 4, "minecraft:lava", "minecraft:lava"], "kubejs:umbrita_dagger": ["dagger", 4, "minecraft:smoke", "minecraft:smoke"], "kubejs:umbrita_sword": ["sword", 4, "minecraft:smoke", "minecraft:smoke"], "kubejs:asa_tempestuosa_spear": ["spear", 4, "minecraft:cloud", "minecraft:cloud"], "kubejs:lobo_sombra_sword": ["sword", 4, "minecraft:enchant", "minecraft:enchant"], "kubejs:draconita_knuckle": ["knuckle", 4, "minecraft:flame", "minecraft:end_rod"], "kubejs:draconita_spear": ["spear", 4, "minecraft:flame", "minecraft:end_rod"], "kubejs:draconita_katana": ["katana", 4, "minecraft:flame", "minecraft:end_rod"], "kubejs:crepusculo_eterno_katana": ["katana", 4, "minecraft:witch", "minecraft:witch"], "kubejs:crepusculo_eterno_claymore": ["claymore", 4, "minecraft:witch", "minecraft:witch"], "kubejs:chama_palida_hammer": ["hammer", 4, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:chama_palida_spear": ["spear", 4, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:viridita_scythe": ["scythe", 4, "minecraft:happy_villager", "minecraft:composter"], "kubejs:viridita_spear": ["spear", 4, "minecraft:happy_villager", "minecraft:composter"], "kubejs:aco_estelar_claymore": ["claymore", 5, "minecraft:crit", "minecraft:crit"], "kubejs:aco_estelar_katana": ["katana", 5, "minecraft:crit", "minecraft:crit"], "kubejs:aco_estelar_sword": ["sword", 5, "minecraft:crit", "minecraft:crit"], "kubejs:estelita_hammer": ["hammer", 5, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:estelita_sword": ["sword", 5, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:estelita_spear": ["spear", 5, "minecraft:end_rod", "minecraft:wax_off"], "kubejs:supernova_double_axe": ["double_axe", 5, "minecraft:lava", "minecraft:lava"], "kubejs:supernova_hammer": ["hammer", 5, "minecraft:lava", "minecraft:lava"], "kubejs:supernova_claymore": ["claymore", 5, "minecraft:lava", "minecraft:lava"], "kubejs:vazio_velado_dagger": ["dagger", 5, "minecraft:smoke", "minecraft:smoke"], "kubejs:vazio_velado_sword": ["sword", 5, "minecraft:smoke", "minecraft:smoke"], "kubejs:cometa_spear": ["spear", 5, "minecraft:cloud", "minecraft:cloud"], "kubejs:eclipse_lupino_sword": ["sword", 5, "minecraft:enchant", "minecraft:enchant"], "kubejs:jade_celestial_knuckle": ["knuckle", 5, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:jade_celestial_spear": ["spear", 5, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:jade_celestial_katana": ["katana", 5, "minecraft:end_rod", "minecraft:end_rod"], "kubejs:eclipsita_katana": ["katana", 5, "minecraft:reverse_portal", "minecraft:witch"], "kubejs:eclipsita_claymore": ["claymore", 5, "minecraft:reverse_portal", "minecraft:witch"], "kubejs:alva_estrela_hammer": ["hammer", 5, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:alva_estrela_spear": ["spear", 5, "minecraft:wax_off", "minecraft:wax_off"], "kubejs:seiva_estelar_scythe": ["scythe", 5, "minecraft:composter", "minecraft:composter"], "kubejs:seiva_estelar_spear": ["spear", 5, "minecraft:composter", "minecraft:composter"], "kubejs:cobre_sword": ["sword", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_katana": ["katana", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_claymore": ["claymore", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_dagger": ["dagger", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_spear": ["spear", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_hammer": ["hammer", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_double_axe": ["double_axe", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_scythe": ["scythe", 1, "minecraft:crit", "minecraft:crit"], "kubejs:cobre_knuckle": ["knuckle", 1, "minecraft:crit", "minecraft:crit"]}, flecha: { 1: 'minecraft:crit', 2: 'minecraft:enchanted_hit', 3: 'minecraft:end_rod',
  4: 'minecraft:soul_fire_flame', 5: 'minecraft:dragon_breath' }, flechas: [] }

function vfxP(level, part, x, y, z, n, espalha, vel) {
  try { level.spawnParticles(part, true, x, y, z, espalha, espalha, espalha, n, vel) } catch (e) { }
}

// Arco do golpe na frente do jogador: graus de 'de' até 'ate', raio r, inclinação (diagonal) e altura
function vfxArco(p, part, de, ate, r, incl, alt, passos) {
  let lv = p.level
  let yaw = p.yRot
  for (let i = 0; i <= passos; i++) {
    let a = de + (ate - de) * i / passos
    let t = (yaw + a) * Math.PI / 180
    let x = p.x - Math.sin(t) * r
    let z = p.z + Math.cos(t) * r
    let y = p.y + alt + (a / 90) * incl
    vfxP(lv, part, x, y, z, 1, 0.0, 0.0)
    if (i % 3 === 0) vfxP(lv, 'minecraft:sweep_attack', x, y, z, 0, 0.0, 0.0)
  }
}

// Som do golpe por tipo de arma (tocado para todos por perto); tom sobe com o tier
const VFX_SOM = {
  claymore: ['minecraft:entity.player.attack.sweep', 0.8], katana: ['minecraft:item.trident.throw', 1.6],
  sword: ['minecraft:entity.player.attack.sweep', 1.1], dagger: ['minecraft:entity.player.attack.crit', 1.5],
  spear: ['minecraft:item.trident.hit', 1.2], hammer: ['minecraft:item.mace.smash_ground', 0.9],
  double_axe: ['minecraft:item.mace.smash_air', 0.8], scythe: ['minecraft:entity.player.attack.sweep', 0.7],
  knuckle: ['minecraft:entity.player.attack.strong', 1.2]
}
const VFX_SOM_TIER = { 3: 'minecraft:block.amethyst_block.hit', 4: 'minecraft:block.respawn_anchor.charge', 5: 'minecraft:entity.evoker.cast_spell' }
function vfxSom(p, alvo, tipo, t) {
  try {
    let s = VFX_SOM[tipo] || VFX_SOM.sword
    let pos = `${alvo.x.toFixed(1)} ${alvo.y.toFixed(1)} ${alvo.z.toFixed(1)}`
    p.server.runCommandSilent(`playsound ${s[0]} player @a ${pos} 0.7 ${(s[1] + t * 0.04).toFixed(2)}`)
    if (VFX_SOM_TIER[t]) p.server.runCommandSilent(`playsound ${VFX_SOM_TIER[t]} player @a ${pos} 0.35 1.4`)
  } catch (e) { }
}

function vfxGolpe(p, alvo, info) {
  let tipo = info[0], t = info[1], mat = info[2], ordem = info[3]
  vfxSom(p, alvo, tipo, t)
  let part = t >= 2 ? mat : (ordem || mat)
  let passos = 6 + t * 2
  let lv = p.level
  if (tipo === 'claymore') vfxArco(p, part, -80, 80, 2.2, 0.6, 1.1, passos + 4)
  else if (tipo === 'katana') { vfxArco(p, part, -60, 60, 1.9, 0.5, 1.3, passos); vfxArco(p, part, 60, -60, 1.7, -0.4, 0.9, passos) }
  else if (tipo === 'sword') vfxArco(p, part, -55, 55, 1.8, 0.45, 1.15, passos)
  else if (tipo === 'dagger') { vfxArco(p, part, -25, 25, 1.4, 0.2, 1.2, 4); vfxP(lv, 'minecraft:crit', alvo.x, alvo.y + alvo.bbHeight * 0.6, alvo.z, 4, 0.2, 0.2) }
  else if (tipo === 'scythe') vfxArco(p, part, -100, 100, 2.4, 0.15, 0.7, passos + 6)
  else if (tipo === 'spear') {
    let t2 = p.yRot * Math.PI / 180
    for (let i = 1; i <= 6; i++) vfxP(lv, part, p.x - Math.sin(t2) * i * 0.5, p.y + 1.3, p.z + Math.cos(t2) * i * 0.5, 1, 0.0, 0.0)
  } else if (tipo === 'hammer' || tipo === 'double_axe') {
    vfxArco(p, part, -70, 70, 2.0, -0.6, 1.2, passos)
    for (let i = 0; i < 12; i++) {
      let a = i * Math.PI / 6
      vfxP(lv, t >= 3 ? 'minecraft:cloud' : 'minecraft:poof', alvo.x + Math.cos(a) * 1.2, alvo.y + 0.1, alvo.z + Math.sin(a) * 1.2, 1, 0.0, 0.02)
    }
  } else if (tipo === 'knuckle') vfxP(lv, part, alvo.x, alvo.y + alvo.bbHeight * 0.6, alvo.z, 6 + t * 2, 0.25, 0.08)
  else vfxArco(p, part, -50, 50, 1.8, 0.4, 1.15, passos)
  if (t >= 4) {
    vfxP(lv, mat, alvo.x, alvo.y + alvo.bbHeight * 0.5, alvo.z, 10 + (t - 4) * 8, 0.35, 0.12)
    if (t >= 5) vfxP(lv, 'minecraft:flash', alvo.x, alvo.y + alvo.bbHeight * 0.5, alvo.z, 1, 0.0, 0.0)
  }
}

function vfxAoBater(event) {
  try {
    let alvo = event.entity
    let src = event.source
    let p = src.player
    if (!alvo || !p) return
    let direto = src.immediate
    if (direto && direto !== p) {
      // flecha nossa acertou: estoura no alvo
      let tier = direto.persistentData.getInt('velaria_vfx')
      if (tier > 0) vfxP(alvo.level, VFX.flecha[tier], alvo.x, alvo.y + alvo.bbHeight * 0.5, alvo.z, 6 + tier * 3, 0.3, 0.08)
      return
    }
    let info = VFX.armas[String(p.mainHandItem.id)]
    if (info) vfxGolpe(p, alvo, info)
  } catch (e) { }
}
try { EntityEvents.afterHurt(vfxAoBater) } catch (e) {
  try { EntityEvents.hurt(vfxAoBater) } catch (e2) { console.warn('[Velária] VFX: evento de dano não encontrado') }
}

// Flechas e virotes: marca quem atirou (tier do jogador) e desenha o rastro enquanto voam
EntityEvents.spawned(event => {
  let e = event.entity
  let tipo = String(e.type)
  if (!/arrow|bolt|quarrel/.test(tipo)) return
  let dono = null
  try { dono = e.getOwner() } catch (x) { }
  if (!dono || !dono.isPlayer()) return
  let tier = VG.velariaTier ? VG.velariaTier(dono) : 1
  e.persistentData.putInt('velaria_vfx', tier)
  VFX.flechas.push({ e: e, fim: dono.server.tickCount + 100, tier: tier })
})

ServerEvents.tick(event => {
  if (VFX.flechas.length === 0 || event.server.tickCount % 2 !== 0) return
  let agora = event.server.tickCount
  VFX.flechas = VFX.flechas.filter(f => {
    let e = f.e
    if (!e || e.isRemoved() || agora > f.fim) return false
    let parado = false
    try { parado = e.getDeltaMovement().lengthSqr() < 0.0025 } catch (x) { }
    if (parado) return false
    vfxP(e.level, VFX.flecha[f.tier], e.x, e.y, e.z, f.tier >= 4 ? 2 : 1, 0.02, 0.0)
    return true
  })
})

// ---------- Aura de quem veste o conjunto completo (tier 3+) ----------
// Quem veste as 4 peças do mesmo conjunto solta partículas do tema da Ordem: runas do Mago, luz do
// Paladino, brasas do Berserker, folhas do Druida, energia do Monge... Tier 3 discreta, 4 média, 5 forte.
const VAU = { conjuntos: {"estanho_pesada": ["minecraft:crit", 1], "estanho_gladiador": ["minecraft:crit", 1], "bronze_solar_pesada": ["minecraft:end_rod", 1], "bronze_solar_radiante": ["minecraft:end_rod", 1], "ferro_brasa_pesada": ["minecraft:small_flame", 1], "ferro_brasa_boreal": ["minecraft:small_flame", 1], "ambar_media": ["minecraft:smoke", 1], "ambar_shinobi": ["minecraft:smoke", 1], "verdecobre_media": ["minecraft:cloud", 1], "verdecobre_errante": ["minecraft:cloud", 1], "prata_lupina_media": ["minecraft:electric_spark", 1], "prata_lupina_agil": ["minecraft:electric_spark", 1], "jade_monastico_media": ["minecraft:wax_on", 1], "jade_monastico_xogum": ["minecraft:wax_on", 1], "ambar_crepuscular_media": ["minecraft:enchant", 1], "ambar_crepuscular_ronin": ["minecraft:enchant", 1], "prata_leve": ["minecraft:end_rod", 1], "prata_celeste": ["minecraft:end_rod", 1], "ambar_runico_leve": ["minecraft:enchant", 1], "ambar_runico_elemental": ["minecraft:enchant", 1], "malaquita_leve": ["minecraft:happy_villager", 1], "malaquita_selvagem": ["minecraft:happy_villager", 1], "oricalco_pesada": ["minecraft:crit", 2], "oricalco_gladiador": ["minecraft:crit", 2], "cobalto_pesada": ["minecraft:end_rod", 2], "cobalto_radiante": ["minecraft:end_rod", 2], "ferro_sombrio_pesada": ["minecraft:small_flame", 2], "ferro_sombrio_boreal": ["minecraft:small_flame", 2], "sombraco_media": ["minecraft:smoke", 2], "sombraco_shinobi": ["minecraft:smoke", 2], "mitril_media": ["minecraft:cloud", 2], "mitril_errante": ["minecraft:cloud", 2], "glaciarita_media": ["minecraft:electric_spark", 2], "glaciarita_agil": ["minecraft:electric_spark", 2], "onix_media": ["minecraft:wax_on", 2], "onix_xogum": ["minecraft:wax_on", 2], "onix_crepuscular_media": ["minecraft:enchant", 2], "onix_crepuscular_ronin": ["minecraft:enchant", 2], "argentea_celeste_leve": ["minecraft:end_rod", 2], "argentea_celeste_celeste": ["minecraft:end_rod", 2], "cobalto_runico_leve": ["minecraft:enchant", 2], "cobalto_runico_elemental": ["minecraft:enchant", 2], "bronze_verdejante_leve": ["minecraft:happy_villager", 2], "bronze_verdejante_selvagem": ["minecraft:happy_villager", 2], "aco_legionario_pesada": ["minecraft:crit", 3], "aco_legionario_gladiador": ["minecraft:crit", 3], "aco_auroral_pesada": ["minecraft:end_rod", 3], "aco_auroral_radiante": ["minecraft:end_rod", 3], "vulcanita_pesada": ["minecraft:small_flame", 3], "vulcanita_boreal": ["minecraft:small_flame", 3], "sangue_velado_media": ["minecraft:smoke", 3], "sangue_velado_shinobi": ["minecraft:smoke", 3], "tempestita_media": ["minecraft:cloud", 3], "tempestita_errante": ["minecraft:cloud", 3], "abissita_media": ["minecraft:electric_spark", 3], "abissita_agil": ["minecraft:electric_spark", 3], "trovejade_media": ["minecraft:wax_on", 3], "trovejade_xogum": ["minecraft:wax_on", 3], "sangrita_media": ["minecraft:enchant", 3], "sangrita_ronin": ["minecraft:enchant", 3], "animita_leve": ["minecraft:end_rod", 3], "animita_celeste": ["minecraft:end_rod", 3], "adamantita_leve": ["minecraft:enchant", 3], "adamantita_elemental": ["minecraft:enchant", 3], "ferrocerne_leve": ["minecraft:happy_villager", 3], "ferrocerne_selvagem": ["minecraft:happy_villager", 3], "escama_legionaria_pesada": ["minecraft:crit", 4], "escama_legionaria_gladiador": ["minecraft:crit", 4], "escama_aurea_pesada": ["minecraft:end_rod", 4], "escama_aurea_radiante": ["minecraft:end_rod", 4], "sangue_dragao_pesada": ["minecraft:small_flame", 4], "sangue_dragao_boreal": ["minecraft:small_flame", 4], "umbrita_media": ["minecraft:smoke", 4], "umbrita_shinobi": ["minecraft:smoke", 4], "asa_tempestuosa_media": ["minecraft:cloud", 4], "asa_tempestuosa_errante": ["minecraft:cloud", 4], "lobo_sombra_media": ["minecraft:electric_spark", 4], "lobo_sombra_agil": ["minecraft:electric_spark", 4], "draconita_media": ["minecraft:wax_on", 4], "draconita_xogum": ["minecraft:wax_on", 4], "crepusculo_eterno_media": ["minecraft:enchant", 4], "crepusculo_eterno_ronin": ["minecraft:enchant", 4], "chama_palida_leve": ["minecraft:end_rod", 4], "chama_palida_celeste": ["minecraft:end_rod", 4], "umbra_arcana_leve": ["minecraft:enchant", 4], "umbra_arcana_elemental": ["minecraft:enchant", 4], "viridita_leve": ["minecraft:happy_villager", 4], "viridita_selvagem": ["minecraft:happy_villager", 4], "aco_estelar_pesada": ["minecraft:crit", 5], "aco_estelar_gladiador": ["minecraft:crit", 5], "estelita_pesada": ["minecraft:end_rod", 5], "estelita_radiante": ["minecraft:end_rod", 5], "supernova_pesada": ["minecraft:small_flame", 5], "supernova_boreal": ["minecraft:small_flame", 5], "vazio_velado_media": ["minecraft:smoke", 5], "vazio_velado_shinobi": ["minecraft:smoke", 5], "cometa_media": ["minecraft:cloud", 5], "cometa_errante": ["minecraft:cloud", 5], "eclipse_lupino_media": ["minecraft:electric_spark", 5], "eclipse_lupino_agil": ["minecraft:electric_spark", 5], "jade_celestial_media": ["minecraft:wax_on", 5], "jade_celestial_xogum": ["minecraft:wax_on", 5], "eclipsita_media": ["minecraft:enchant", 5], "eclipsita_ronin": ["minecraft:enchant", 5], "alva_estrela_leve": ["minecraft:end_rod", 5], "alva_estrela_celeste": ["minecraft:end_rod", 5], "vacuita_leve": ["minecraft:enchant", 5], "vacuita_elemental": ["minecraft:enchant", 5], "seiva_estelar_leve": ["minecraft:happy_villager", 5], "seiva_estelar_selvagem": ["minecraft:happy_villager", 5]}, pecas: ['helmet', 'chestplate', 'leggings', 'boots'] }
VAU.slots = (() => {
  try { return (c => [c.HEAD, c.CHEST, c.LEGS, c.FEET])(Java.loadClass('net.minecraft.world.entity.EquipmentSlot')) }
  catch (e) { return ['head', 'chest', 'legs', 'feet'] }
})()

function vauConjunto(p) {
  let id0 = null
  for (let i = 0; i < 4; i++) {
    let id = String(p.getItemBySlot(VAU.slots[i]).id)
    let suf = '_' + VAU.pecas[i]
    if (!id.startsWith('kubejs:') || !id.endsWith(suf)) return null
    let c = id.substring(7, id.length - suf.length)
    if (id0 === null) id0 = c
    else if (id0 !== c) return null
  }
  return id0
}
VG.velariaConjuntoVestido = vauConjunto

PlayerEvents.tick(event => {
  let p = event.player
  let t = p.server.tickCount
  if (t % 5 !== 2 || p.isSpectator() || p.isInvisible()) return
  let c = vauConjunto(p)
  if (!c) return
  let d = VAU.conjuntos[c]
  if (!d || d[1] < 3) return
  if (d[1] === 3 && t % 10 !== 2) return
  let n = d[1] >= 5 ? 2 : 1
  for (let i = 0; i < n; i++) {
    let a = Math.random() * Math.PI * 2
    let r = 0.45 + Math.random() * 0.25
    vfxP(p.level, d[0], p.x + Math.cos(a) * r, p.y + 0.3 + Math.random() * 1.5, p.z + Math.sin(a) * r, 1, 0.0, 0.01)
  }
})
