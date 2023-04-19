<script setup lang="ts">

const records = ref([] as any[]);
const { state } = useStore();

const fetchRecords = async () => {
    const { data } = await useFetch(
        `/api/records?uid=${state.user.ref}`
    ).json()
    records.value = unref(data);
}

const deleteRecord = async (item: any) => {
    await useFetch(
        `/api/records/delete?key=${item.key}`
    )
    await fetchRecords();
}

onMounted(async () => {
    setTimeout(() => {
        fetchRecords();
    }, 1000);
});

</script>

<template>
    <div row>
        <div class="col start h-86vh w-1/4">
            <div v-for="item in records" v-if="records" col center w-64>
                <div row center m-2>
                    <h1 text-caption mx-1>{{ new Date(item.created_at).toLocaleDateString() }}</h1>
                    <Icon class="text-warning hover:text-danger cursor-pointer scale" icon="mdi-delete"
                        @click="deleteRecord(item)" />

                </div>
                <audio controls w-48 invert m-2 :src="item.url" />
            </div>
        </div>
        <div grid3 w-full>
            <HAudio v-for="i in [1, 2, 3, 4, 5, 6, 7, 8, 9]" @upload="fetchRecords" :id="i" />
        </div>
    </div>
    <footer h-24></footer>
</template>
