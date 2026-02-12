// Event System (click, hover, proximity)
import * as THREE from 'three'
import type { SceneEvent } from './types'

export class EventSystem {
  private listeners: Map<string, Set<(event: SceneEvent) => void>> = new Map()
  private raycaster: THREE.Raycaster = new THREE.Raycaster()
  private mouse: THREE.Vector2 = new THREE.Vector2()
  private hoveredObject: THREE.Object3D | null = null

  constructor() {
    this.raycaster.params.Line = { threshold: 0.1 }
  }

  on(eventType: SceneEvent['type'], callback: (event: SceneEvent) => void) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set())
    }
    this.listeners.get(eventType)!.add(callback)
  }

  off(eventType: SceneEvent['type'], callback: (event: SceneEvent) => void) {
    const callbacks = this.listeners.get(eventType)
    if (callbacks) {
      callbacks.delete(callback)
    }
  }

  emit(event: SceneEvent) {
    const callbacks = this.listeners.get(event.type)
    if (callbacks) {
      callbacks.forEach(callback => callback(event))
    }
  }

  handleClick(
    event: MouseEvent,
    camera: THREE.Camera,
    objects: THREE.Object3D[]
  ) {
    this.updateMousePosition(event)
    this.raycaster.setFromCamera(this.mouse, camera)
    
    const intersects = this.raycaster.intersectObjects(objects, true)
    
    if (intersects.length > 0) {
      this.emit({
        type: 'click',
        target: intersects[0].object,
        position: intersects[0].point
      })
    }
  }

  handleHover(
    event: MouseEvent,
    camera: THREE.Camera,
    objects: THREE.Object3D[]
  ) {
    this.updateMousePosition(event)
    this.raycaster.setFromCamera(this.mouse, camera)
    
    const intersects = this.raycaster.intersectObjects(objects, true)
    
    if (intersects.length > 0) {
      const object = intersects[0].object
      
      if (this.hoveredObject !== object) {
        this.hoveredObject = object
        this.emit({
          type: 'hover',
          target: object,
          position: intersects[0].point
        })
      }
    } else if (this.hoveredObject) {
      this.hoveredObject = null
    }
  }

  checkProximity(
    position: THREE.Vector3,
    objects: THREE.Object3D[],
    threshold: number = 2
  ) {
    objects.forEach(object => {
      const distance = position.distanceTo(object.position)
      
      if (distance < threshold) {
        this.emit({
          type: 'proximity',
          target: object,
          position: object.position,
          data: { distance }
        })
      }
    })
  }

  private updateMousePosition(event: MouseEvent) {
    this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1
    this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1
  }
}
