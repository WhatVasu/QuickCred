// Wallet management dialog
let walletDialog = null;

// Initialize wallet dialog
document.addEventListener('DOMContentLoaded', function() {
    const dialogHtml = `
        <div id="walletModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 hidden overflow-y-auto h-full w-full">
            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                <div class="mt-3">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg leading-6 font-medium text-gray-900">Manage Wallet</h3>
                        <button onclick="hideWalletModal()" class="text-gray-400 hover:text-gray-500">
                            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                    </div>
                    <div class="mt-4">
                        <p class="text-sm text-gray-500">Current Balance: ₹<span id="currentBalance">0</span></p>
                        <div class="mt-4">
                            <label class="block text-sm font-medium text-gray-700">Amount (₹)</label>
                            <input type="number" id="walletAmount" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" min="0" max="1000000">
                        </div>
                        <div class="mt-4 flex gap-2">
                            <button onclick="updateWallet('add')" class="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">Add Money</button>
                            <button onclick="updateWallet('subtract')" class="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">Remove Money</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add dialog to body
    const div = document.createElement('div');
    div.innerHTML = dialogHtml;
    document.body.appendChild(div);
    
    // Store reference to modal
    walletDialog = document.getElementById('walletModal');
});

function showWalletModal() {
    if (!walletDialog) return;
    walletDialog.classList.remove('hidden');
    // Update current balance display
    if (currentUser) {
        document.getElementById('currentBalance').textContent = currentUser.wallet_balance.toLocaleString();
    }
}

function hideWalletModal() {
    if (!walletDialog) return;
    walletDialog.classList.add('hidden');
}

async function updateWallet(operation) {
    const amount = parseFloat(document.getElementById('walletAmount').value);
    if (!amount || isNaN(amount) || amount <= 0) {
        alert('Please enter a valid amount');
        return;
    }

    try {
        const response = await apiCall('/transactions/update-wallet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                operation,
                amount 
            })
        });

        const data = await response.json();
        if (response.ok) {
            // Update local user data and UI
            currentUser.wallet_balance = data.new_balance;
            document.getElementById('currentBalance').textContent = data.new_balance.toLocaleString();
            
            // Update all wallet displays
            const walletDisplays = document.querySelectorAll('[id$="-wallet"]');
            walletDisplays.forEach(display => {
                display.textContent = '₹' + data.new_balance.toLocaleString();
            });

            hideWalletModal();
        } else {
            alert(data.error || 'Failed to update wallet');
        }
    } catch (error) {
        console.error('Wallet update error:', error);
        alert('Failed to update wallet. Please try again.');
    }
}