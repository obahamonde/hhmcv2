
<script setup>
import { useSequencerStore } from '~/composables'
import * as Tone from 'tone'
const sequencerStore = useSequencerStore()
const synth = new Tone.Sampler({
    urls: {
        C4: "C4.mp3",
        A4: "A4.mp3",
        C5: "C5.mp3",
        A5: "A5.mp3",
        C6: "C6.mp3",
        A6: "A6.mp3",
    },
    release: 1,
    baseUrl: "https://tonejs.github.io/audio/salamander/",
}).toDestination();

onBeforeMount(() => {
    sequencerStore.initMelody()
})
</script>
<template>
    <v-layout>
        <v-main class="page">
            <Sequencer :synth="synth" />
        </v-main>
    </v-layout>
</template>
  