import { defineStore } from 'pinia'

// Global state for the sequencer
export const useSequencerStore = defineStore('sequencerStore', {

    state: () => ({
        melodyLength: 40,
        melody: [] as number[],
        lowestNote: 60,     // C4
        highestNote: 83,    // B5
        notes: [] as number[],
    }),
    getters: {
        getNoteAtPosition: (state: any) => (position: number) => state.melody[position],
        getMelodyNotes: (state: any): number => state.melody.filter(note => note > 0).length, 
        getMelody: (state: any) => state.melody.filter(note => note > 0),
    },
    actions: {
        initMelody() {
            for (let i = this.lowestNote; i <= this.highestNote; ++i) {
                this.notes.push(i)
            }
            this.notes.reverse()

            for (let i = 0; i < this.melodyLength; ++i) {
                this.melody.push(0)
            }
        },

        changeNoteAtPosition(position, note) {
            this.melody[position] = note
        },

        resetMelody() {
            for (let i = 0; i < this.melodyLength; ++i) {
                this.melody[i] = 0
            }
        }
    }
})

