// Internal Timeline System
import type { TimelineEvent } from './types'

export class Timeline {
  private events: TimelineEvent[] = []
  private currentTime: number = 0
  private isPlaying: boolean = false
  private startTime: number = 0
  private pausedTime: number = 0

  addEvent(event: TimelineEvent) {
    this.events.push(event)
    this.events.sort((a, b) => a.time - b.time)
  }

  removeEvent(name: string) {
    this.events = this.events.filter(e => e.name !== name)
  }

  play() {
    if (!this.isPlaying) {
      this.isPlaying = true
      this.startTime = Date.now() - this.pausedTime
      this.tick()
    }
  }

  pause() {
    if (this.isPlaying) {
      this.isPlaying = false
      this.pausedTime = Date.now() - this.startTime
    }
  }

  stop() {
    this.isPlaying = false
    this.currentTime = 0
    this.pausedTime = 0
  }

  seek(time: number) {
    this.currentTime = time
    this.pausedTime = time
    this.startTime = Date.now() - time
  }

  private tick() {
    if (!this.isPlaying) return

    this.currentTime = Date.now() - this.startTime

    // Execute events that should have triggered
    this.events.forEach(event => {
      if (event.time <= this.currentTime && event.time > this.currentTime - 100) {
        event.action()
      }
    })

    requestAnimationFrame(() => this.tick())
  }

  getCurrentTime() {
    return this.currentTime
  }

  getEvents() {
    return [...this.events]
  }

  clear() {
    this.events = []
    this.stop()
  }
}
