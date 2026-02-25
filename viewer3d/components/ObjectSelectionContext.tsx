'use client'

/**
 * ObjectSelectionContext - Estado global liviano para selección de objetos 3D.
 * 
 * selectedId: ID del objeto actualmente seleccionado (null = ninguno)
 * pendingMove: posición destino pendiente de consumir
 */

import { createContext, useContext, useState, useCallback, useRef } from 'react'

interface ObjectSelectionState {
  selectedId: string | null
  setSelected: (id: string | null) => void
  pendingMove: [number, number, number] | null
  requestMove: (pos: [number, number, number]) => void
  consumeMove: () => [number, number, number] | null
}

const ObjectSelectionContext = createContext<ObjectSelectionState>({
  selectedId: null,
  setSelected: () => {},
  pendingMove: null,
  requestMove: () => {},
  consumeMove: () => null
})

export function ObjectSelectionProvider({ children }: { children: React.ReactNode }) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const pendingMoveRef = useRef<[number, number, number] | null>(null)
  const [pendingMove, setPendingMove] = useState<[number, number, number] | null>(null)

  const setSelected = useCallback((id: string | null) => {
    setSelectedId(id)
    if (id === null) {
      pendingMoveRef.current = null
      setPendingMove(null)
    }
  }, [])

  const requestMove = useCallback((pos: [number, number, number]) => {
    pendingMoveRef.current = pos
    setPendingMove(pos)
  }, [])

  const consumeMove = useCallback(() => {
    const move = pendingMoveRef.current
    pendingMoveRef.current = null
    setPendingMove(null)
    return move
  }, [])

  return (
    <ObjectSelectionContext.Provider value={{ selectedId, setSelected, pendingMove, requestMove, consumeMove }}>
      {children}
    </ObjectSelectionContext.Provider>
  )
}

export function useObjectSelection() {
  return useContext(ObjectSelectionContext)
}
