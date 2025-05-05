<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <button @click="$emit('close')" class="close-button">&times;</button>

      <h2>Payment Details</h2>

      <div class="form-group">
        <label>Service Name:</label>
        <input
          type="text"
          v-model="localService.name"
          class="form-control"
          disabled
        />
      </div>

      <div class="form-group">
        <label>Price:</label>
        <input
          type="text"
          :value="formattedPrice"
          class="form-control"
          disabled
        />
      </div>

      <div class="qr-code-section">
        <h3>Scan to Pay</h3>

        <img
          src="@/assets/qr-code.png"
          alt="Payment QR Code"
          class="qr-code-image"
        />
      </div>

      <div class="button-group">
        <button @click="handlePayment" class="btn btn-primary">Pay</button>
        <button @click="$emit('close')" class="btn btn-secondary">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    service: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      localService: { ...this.service },
    };
  },
  computed: {
    formattedPrice() {
      return `₹${this.localService.price.toFixed(2)}`;
    },
  },
  methods: {
    handlePayment() {
      this.$emit("pay", this.service);
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 90%;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.close-button {
  background: transparent;
  border: none;
  font-size: 1.5em;
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  color: #aaa;
  transition: color 0.3s;
}

.close-button:hover {
  color: #000;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.qr-code-section {
  text-align: center;
  margin: 20px 0;
}

.qr-code-section h3 {
  margin-bottom: 10px;
  color: #333;
}

.qr-code-image {
  width: 200px;
  height: 200px;
  border: 2px solid #ddd;
  border-radius: 8px;
  object-fit: cover;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 10px 16px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  color: #fff;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
