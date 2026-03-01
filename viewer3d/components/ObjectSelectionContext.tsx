'use client'

/**
 * ObjectSelectionContext - Estado global liviano para selección de objetos 3D.
 * 
 * selectedId: ID del objeto actualmente seleccionado (null = ninguno)
 * pendingMove: posición destino pendiente de consumir
 * blockMoved: true cuando algún bloque de Puma Punku fue movido (activa reveal de estructura)
 */

import { createContext, useContext, useState, useCallback, useRef } from 'react'

interface ObjectSelectionState {
  selectedId: string | null
  setSelected: (id: string | null) => void
  pendingMove: [number, number, number] | null
  requestMove: (pos: [number, number, number]) => void
  consumeMove: () => [number, number, number] | null
  blockMoved: boolean
  notifyBlockMoved: () => void
}

const ObjectSelectionContext = createContext<ObjectSelectionState>({
  selectedId: null,
  setSelected: () => {},
  pendingMove: null,
  requestMove: () => {},
  consumeMove: () => null,
  blockMoved: false,
  notifyBlockMoved: () => {}
})

interface ObjectSelectionProviderProps {
  children: React.ReactNode
  onBlockMoved?: () => void
}

export function ObjectSelectionProvider({ children, onBlockMoved }: ObjectSelectionProviderProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const pendingMoveRef = useRef<[number, number, number] | null>(null)
  const [pendingMove, setPendingMove] = useState<[number, number, number] | null>(null)
  
  // Estado persistente de blockMoved
  const [blockMoved, setBlockMoved] = useState(() => {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('puma_punku_block_moved') === 'true'
    }
    return false
  })
  
  const onBlockMovedRef = useRef(onBlockMoved)
  onBlockMovedRef.current = onBlockMoved

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

  const notifyBlockMoved = useCallback(() => {
    setBlockMoved(true)
    if (typeof window !== 'undefined') {
      sessionStorage.setItem('puma_punku_block_moved', 'true')
    }
    onBlockMovedRef.current?.()
  }, [])

  return (
    <ObjectSelectionContext.Provider value={{ selectedId, setSelected, pendingMove, requestMove, consumeMove, blockMoved, notifyBlockMoved }}>
      {children}
    </ObjectSelectionContext.Provider>
  )
}

export function useObjectSelection() {
  return useContext(ObjectSelectionContext)
}
