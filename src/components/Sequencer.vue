<script setup>
import { useSequencerStore } from "~/composables"
const props = defineProps({
    synth: null
})

const sequencerStore = useSequencerStore()
</script>



<template>
    <div>
        <SequencerControls :synth="props.synth" />
        <div class="sequencer">
            <PianoColumn />
            <NoteColumn v-for="(note, i) in sequencerStore.melodyLength" :position-in-melody=i :synth="props.synth" />
        </div>
    </div>
</template>
  
  
<style scoped lang="sass">
  .sequencer
    display: flex
    flex-direction: row
    overflow-x: auto
  </style>
  