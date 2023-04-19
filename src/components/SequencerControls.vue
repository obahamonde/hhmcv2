
<script setup>
import { useSequencerStore } from "~/composables"
import { midiNoteToString } from "~/composables"
import { usePianoStore } from "~/composables";


const props = defineProps({
    synth: null
})

const sequencerStore = useSequencerStore()
const store = usePianoStore()

function play() {
    if (!store.playing) {
        console.log("started playing")
        store.playPosition = -1
        store.playing = true
        store.sequencerPlaying = true
        store.callbackId = setInterval(playNote, 200)
    } else {
        stop()
    }
}

function stop() {
    store.stopPlaying()
}

function playNote() {
    if (store.playPosition < sequencerStore.melodyLength) {
        store.playPosition++
        if (sequencerStore.melody[store.playPosition] > 0)
            props.synth.triggerAttackRelease(midiNoteToString(sequencerStore.melody[store.playPosition]), "8n");
        // console.log("playing note" + store.playPosition)
    } else {
        stop()
    }
}
</script>


<template>
    <div>
        <v-btn variant="outlined" ma-2 icon @click="play()">
            <v-icon v-if="store.playing">
                mdi-stop
            </v-icon>
            <v-icon v-else>
                mdi-play
            </v-icon>
        </v-btn>
        <v-btn variant="outlined" icon ma-2 @click="sequencerStore.resetMelody()">
            <v-icon>mdi-trash-can-outline</v-icon>
        </v-btn>
    </div>
</template>
  
<style scoped></style>