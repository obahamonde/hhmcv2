<script setup lang="ts">
import { IllestWaveform } from "1llest-waveform-vue";
import type { IllestWaveformProps } from "1llest-waveform-vue";
import { Icon } from "@iconify/vue"
import "1llest-waveform-vue/lib/style.css";

const audioStream = ref<MediaStream | null>(null);
const isPlaying = ref<boolean>(false);
const enabled = ref<boolean>(false);
const audioFile = ref(null as File | null);
const init = ref(false);
const fetched = ref(false);
const playing = ref(false);
const finished = ref(false);
const ready = ref(false);
const currentTime = ref("0:00");
const durationTime = ref("0:00");
const waveformRef = ref<typeof IllestWaveform | null>(null);

const { state } = useStore()

const play = () => {
  if (enabled.value) {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(async (stream) => {
        audioStream.value = stream;
        isPlaying.value = true;

        const audioChunks = ref<BlobPart[]>([]);
        const mediaRecorder = new MediaRecorder(audioStream.value);

        mediaRecorder.addEventListener("dataavailable", (event) => {
          audioChunks.value.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
          const audioBlob = new Blob(audioChunks.value);
          audioFile.value = new File([audioBlob], "audio.webm", {
            type: "audio/webm",
          });
        });

        mediaRecorder.start();
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

const stop = () => {
  if (audioStream.value) {
    const tracks = audioStream.value.getTracks();
    tracks.forEach((track) => {
      track.stop();
    });
    audioStream.value = null;
    isPlaying.value = false;
    audioFile.value = null;
    audioURL.value = "";
  }
};

const audioURL = ref("");

watchEffect(() => {
  if (audioFile.value) {
    audioURL.value = URL.createObjectURL(audioFile.value);
  }
});

const waveOptions = reactive<IllestWaveformProps>({
  url: computed(() => audioURL.value),
});

onMounted(() => {
  watchEffect(() => {
    if (enabled.value) {
      play();
    } else {
      stop();
    }
  });
});

const emit = defineEmits(["upload"])

onBeforeUnmount(() => {
  stop();
});

onMounted(() => {
  getCurrentTime();
});

const initHandler = (v: boolean) => {
  init.value = v;
};

const fetchedHandler = (v: boolean) => {
  fetched.value = v;
};

const readyHandler = (v: boolean) => {
  ready.value = v;
  getDuration();
};

const finishHandler = (v: boolean) => {
  finished.value = v;
};

const clickHandler = (el: HTMLElement, time: number) => {
  console.log(el, time);
};

const playWave = () => {
  waveformRef.value!.play();
};

const replay = () => {
  waveformRef.value!.replay();
};

const pauseWave = () => {
  waveformRef.value!.pause();
};

const getCurrentTime = () => {
  watchEffect(() => {
    if (waveformRef.value === null || !ready.value) return;
    const current = waveformRef.value!.getCurrentTime();
    currentTime.value = current;
  });
};

const getDuration = () => {
  const duration = waveformRef.value!.getDuration();
  durationTime.value = duration;
};

const uploadWave = async() => {
    const formdata = new FormData();
    formdata.append("file", audioFile.value as File);
    const { data } = await useFetch(`api/upload?uid=${state.user.ref}`, {
      method: "POST",
      body: formdata,
    }).json()
    const { url } = unref(data)
    console.log(url)
    audioURL.value = url;
    emit("upload")
  };

</script>
<template>
  <main class="col center sh">
    <section class="row center gap-4">
      <button @click="enabled = !enabled">
        <Icon icon="mdi-microphone"  hover:text-primary  cp scale v-if="!enabled" />
        <Icon icon="mdi-microphone-off"  hover:text-primary  cp scale v-else />
      </button>

      <div>
        <button @click="pauseWave" v-if="playing">
          <Icon icon="mdi-pause"  cp scale hover:text-primary />
        </button>
        <button @click="playWave" v-else>
          <Icon icon="mdi-play"  cp scale hover:text-primary />
        </button>
      </div>
      <button >
        <Icon icon="mdi-refresh" @click="replay"  cp scale v-if="playing" />
        <Icon icon="mdi-upload" cp scale v-else @click="uploadWave" />
      </button>
    </section>
    <div v-if="audioURL" >
      <IllestWaveform ref="waveformRef" class="w-2/3 h-2/3"
      v-bind="waveOptions" @on-init="initHandler" @on-fetched="fetchedHandler"
        @on-ready="readyHandler" @on-play="(v: boolean) => (playing = v)" @on-pause="(v: boolean) => (playing = v)"
        @on-finish="finishHandler" @on-click="clickHandler" />
      <div text-xs text-center>{{ currentTime }} - {{ durationTime }}</div>
    </div>
  </main>
  
</template>
<style global>
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

</style>