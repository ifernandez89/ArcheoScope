/**
 * GeometryField - Campo geométrico invisible revelable
 * Líneas etéreas, sin texto, sin números, estructura latente
 */

import * as THREE from 'three'

export class GeometryField {
  private scene: THREE.Scene
  private linesGroup: THREE.Group
  private visible: boolean = false
  private opacity: number = 0
  private targetOpacity: number = 0
  private fadeSpeed: number = 0.02

  constructor(scene: THREE.Scene) {
    this.scene = scene
    this.linesGroup = new THREE.Group()
    this.linesGroup.name = 'GeometryField'
    this.scene.add(this.linesGroup)
    
    this.createGeometricLines()
  }

  /**
   * Crear líneas geométricas etéreas
   */
  private createGeometricLines() {
    const material = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.15,
      depthTest: false,
      depthWrite: false
    })

    const lineLength = 100

    // Línea cardinal Norte-Sur
    const northSouth = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0.01, -lineLength),
      new THREE.Vector3(0, 0.01, lineLength)
    ])
    const nsLine = new THREE.Line(northSouth, material)
    nsLine.name = 'NorthSouth'
    this.linesGroup.add(nsLine)

    // Línea cardinal Este-Oeste
    const eastWest = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-lineLength, 0.01, 0),
      new THREE.Vector3(lineLength, 0.01, 0)
    ])
    const ewLine = new THREE.Line(eastWest, material)
    ewLine.name = 'EastWest'
    this.linesGroup.add(ewLine)

    // Círculo de horizonte
    const horizonPoints: THREE.Vector3[] = []
    const horizonRadius = 80
    const segments = 64
    for (let i = 0; i <= segments; i++) {
      const angle = (i / segments) * Math.PI * 2
      horizonPoints.push(new THREE.Vector3(
        Math.cos(angle) * horizonRadius,
        0.01,
        Math.sin(angle) * horizonRadius
      ))
    }
    const horizonGeometry = new THREE.BufferGeometry().setFromPoints(horizonPoints)
    const horizonLine = new THREE.Line(horizonGeometry, material)
    horizonLine.name = 'Horizon'
    this.linesGroup.add(horizonLine)

    // Círculos concéntricos (opcional, más sutil)
    for (let r = 20; r < 80; r += 20) {
      const circlePoints: THREE.Vector3[] = []
      for (let i = 0; i <= segments; i++) {
        const angle = (i / segments) * Math.PI * 2
        circlePoints.push(new THREE.Vector3(
          Math.cos(angle) * r,
          0.01,
          Math.sin(angle) * r
        ))
      }
      const circleGeometry = new THREE.BufferGeometry().setFromPoints(circlePoints)
      const circleMaterial = new THREE.LineBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.05,
        depthTest: false,
        depthWrite: false
      })
      const circle = new THREE.Line(circleGeometry, circleMaterial)
      circle.name = `Circle_${r}`
      this.linesGroup.add(circle)
    }

    // Inicialmente invisible
    this.linesGroup.visible = false
  }

  /**
   * Actualizar eje solar proyectado
   */
  updateSolarAxis(sunDirection: THREE.Vector3) {
    // Remover eje solar anterior si existe
    const oldAxis = this.linesGroup.getObjectByName('SolarAxis')
    if (oldAxis) {
      this.linesGroup.remove(oldAxis)
    }

    // Proyectar dirección solar al plano
    const solarGround = sunDirection.clone()
    solarGround.y = 0
    solarGround.normalize()
    solarGround.multiplyScalar(90)

    // Crear línea de eje solar
    const solarAxisGeometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0.02, 0),
      new THREE.Vector3(solarGround.x, 0.02, solarGround.z)
    ])
    const solarMaterial = new THREE.LineBasicMaterial({
      color: 0xffaa00,
      transparent: true,
      opacity: 0.2,
      depthTest: false,
      depthWrite: false
    })
    const solarAxis = new THREE.Line(solarAxisGeometry, solarMaterial)
    solarAxis.name = 'SolarAxis'
    this.linesGroup.add(solarAxis)
  }

  /**
   * Toggle visibilidad
   */
  toggle() {
    this.visible = !this.visible
    this.targetOpacity = this.visible ? 1 : 0
  }

  /**
   * Mostrar campo
   */
  show() {
    this.visible = true
    this.targetOpacity = 1
  }

  /**
   * Ocultar campo
   */
  hide() {
    this.visible = false
    this.targetOpacity = 0
  }

  /**
   * Actualizar opacidad con fade suave
   */
  update(deltaTime: number) {
    // Fade suave
    this.opacity += (this.targetOpacity - this.opacity) * this.fadeSpeed

    // Actualizar visibilidad del grupo
    if (this.opacity > 0.01) {
      this.linesGroup.visible = true
      
      // Actualizar opacidad de todas las líneas
      this.linesGroup.traverse((child) => {
        if (child instanceof THREE.Line) {
          const material = child.material as THREE.LineBasicMaterial
          if (child.name === 'SolarAxis') {
            material.opacity = 0.2 * this.opacity
          } else if (child.name.startsWith('Circle_')) {
            material.opacity = 0.05 * this.opacity
          } else {
            material.opacity = 0.15 * this.opacity
          }
        }
      })
    } else {
      this.linesGroup.visible = false
    }
  }

  /**
   * Verificar si está visible
   */
  isVisible(): boolean {
    return this.visible
  }
}
