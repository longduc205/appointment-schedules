document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('specialty').addEventListener('change', function() {
        const specialtyId = this.value;
        const doctorSelect = document.getElementById('doctor');
        
        // Clear doctor options
        doctorSelect.innerHTML = '<option value="">Select doctor</option>';
        
        if (specialtyId) {
            // Fetch doctors by specialty
            fetch(`/api/doctors/${specialtyId}`)
                .then(response => response.json())
                .then(doctors => {
                    doctors.forEach(doctor => {
                        const option = document.createElement('option');
                        option.value = doctor.doctor_id;
                        option.textContent = doctor.full_name;
                        doctorSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching doctors:', error);
                });
        }
    });
});