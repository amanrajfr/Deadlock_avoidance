const si = require('systeminformation');
const fs = require('fs');

async function insertData(processes) {
  try {
    const existingProcesses = new Set();
    const csvRows = [];

    for (const process of processes) {
      const { name, cpu, mem, pids } = process;

      if (existingProcesses.has(name)) {
        console.log(`Skipping duplicate process name: ${name}`);
        continue;
      }

      try {
        const cpuData = await si.currentLoad();
        const memoryData = await si.mem();
        const gpuData = await si.graphics();

        const cpu_usage_alloc = cpu || 0;
        const memory_usage_alloc = mem || 0;
        const gpu_usage_alloc = 0;
        const cpu_usage_max = cpuData.currentload || 1;
        const memory_usage_max = memoryData.used / memoryData.total * 100 || 0;
        const gpu_usage_max = gpu_usage_alloc;

        if (name !== "System Idle Process") { // Exclude "System Idle Process"
          const csvRow = `${name || 'Unknown'},${cpu_usage_alloc},${memory_usage_alloc},${gpu_usage_alloc},${cpu_usage_max},${memory_usage_max},${gpu_usage_max}`;
          csvRows.push(csvRow);

          existingProcesses.add(name);
        }
      } catch (error) {
        console.error('Error processing data for process:', name, error);
      }
    }

    // Write data to CSV file
    fs.writeFileSync('output.csv', csvRows.join('\n'));
    console.log('Data written to output.csv successfully');
  } catch (error) {
    console.error('Error inserting data:', error);
  }
}

async function processData() {
  try {
    const processes = await si.processes();
    await insertData(processes.list);
  } catch (error) {
    console.error('Error fetching process data:', error);
  }
}

processData();

