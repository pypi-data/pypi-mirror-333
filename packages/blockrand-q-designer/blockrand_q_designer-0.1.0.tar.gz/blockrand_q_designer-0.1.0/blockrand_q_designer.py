import itertools
import random
import numpy as np
import csv

class LCMSQueueDesign:
    def __init__(self, factors, levels, block_size, base_name="sample_", starting_index=1, max_retries=10):
        """
        factors: list of factor names (e.g. ['Fraction', 'Treatment', 'Replicate'])
        levels: list of number of levels for each factor
        block_size: desired block size
        base_name: base string for sample IDs
        starting_index: starting index for sample IDs
        max_retries: number of attempts for partitioning the space
        """
        self.factors = factors
        self.levels = levels
        self.block_size = block_size
        self.base_name = base_name
        self.starting_index = starting_index
        self.max_retries = max_retries
        self.sample_dict = {}      # {sample_id: sample tuple}
        self.sample_name_dict = {}  # {sample_id: string ID}
        self.blocks = []           # List of blocks (each is a tuple or list of sample_ids)
        self.labels = {}           # Optional label mappings for factors
        
        self._generate_sample_space()
        self._initialize_blocks()

    def _generate_sample_space(self):
        combinations = list(itertools.product(*[range(l) for l in self.levels]))
        for i, sample in enumerate(combinations, start = 1):
            self.sample_dict[i] = tuple(sample)
            self.sample_name_dict[i] = f"{self.base_name}{i + self.starting_index:03d}"

    def _is_valid_block(self, block):
        """
        Validate a block sample.
        - For a factor where number of levels == block_size (strict factor): require all values are distinct.
        - For a factor where number of levels < block_size (flexible factor): for complete blocks, require that
          the counts differ by at most 1; for incomplete blocks, the constraint is relaxed.
        - For a factor where number of levels > block_size (distinct factor): require that all values in the block
          are distinct.
        """
        block_matrix = np.array([self.sample_dict[s] for s in block])
        block_len = len(block)
        for idx, num_levels in enumerate(self.levels):
            values = block_matrix[:, idx]
            # Strict factor: exactly block_size levels (for full blocks, require exactly block_size distinct values)
            if num_levels == self.block_size:
                if len(set(values)) != block_len:
                    return False
            # Flexible factor: fewer levels than block_size.
            elif num_levels < self.block_size:
                if block_len == self.block_size:  # Only enforce balance in complete blocks
                    counts = {level: 0 for level in range(num_levels)}
                    for val in values:
                        counts[val] += 1
                    count_values = list(counts.values())
                    if max(count_values) - min(count_values) > 1:
                        return False
                # For incomplete blocks, we relax this constraint.
            # Distinct factor: more levels than block_size; require all values in the block are distinct.
            else:  # num_levels > self.block_size
                if len(set(values)) != block_len:
                    return False
        return True

    def _find_valid_blocks(self, seed, available_samples):
        potential_blocks = []
        for sample_comb in itertools.combinations(available_samples - {seed}, 
                                                    min(self.block_size - 1, len(available_samples) - 1)):
            block = (seed,) + sample_comb
            if self._is_valid_block(block):
                potential_blocks.append(block)
        return potential_blocks

    def _initialize_blocks(self):
        for attempt in range(self.max_retries):
            available_samples = set(self.sample_dict.keys())
            self.blocks = []

            while available_samples:
                if len(available_samples) < self.block_size:
                    # If remaining samples are fewer than block_size, put them in a final block (no constraint checking).
                    final_block = tuple(available_samples)
                    self.blocks.append(final_block)
                    print(f"Final block (incomplete): {final_block}")
                    return  # Successfully partitioned

                seed = random.choice(list(available_samples))
                candidate_blocks = self._find_valid_blocks(seed, available_samples)
                if not candidate_blocks:
                    print(f"Attempt {attempt + 1}: Failed, retrying...")
                    break
                chosen_block = random.choice(candidate_blocks)
                self.blocks.append(chosen_block)
                for sample in chosen_block:
                    available_samples.remove(sample)
                print(f"Chosen block {len(self.blocks)}: {chosen_block}. {len(available_samples)} samples remaining.")

            if not available_samples:
                return  # Successfully partitioned

        raise Exception("Failed to partition the space after max retries.")

    def intra_block_reshuffle(self, iterations=10):
        """
        Intra-block reshuffling to optimize dispersion of factor levels in the flattened queue.
        The cost function comprises two terms:
         1. Adjacent Penalty: Penalizes adjacent samples (in flattened order) with the same level.
         2. Position Balance Penalty: For complete blocks, penalizes deviations from the ideal frequency 
            of levels at each block position.
        """
        def flattened_order(blocks):
            order = []
            for block in blocks:
                order.extend(block)
            return order

        def cost(flat_order, blocks):
            cost_adj = 0
            # Adjacent penalty in the flattened order.
            for i in range(len(flat_order) - 1):
                sample1 = self.sample_dict[flat_order[i]]
                sample2 = self.sample_dict[flat_order[i+1]]
                for f in range(len(self.factors)):
                    if sample1[f] == sample2[f]:
                        cost_adj += 1

            cost_pos = 0
            # Consider only complete blocks for position balance.
            complete_blocks = [block for block in blocks if len(block) == self.block_size]
            if complete_blocks:
                for pos in range(self.block_size):
                    for f in range(len(self.factors)):
                        freq = {}  # Frequency of each level at this position for factor f.
                        for block in complete_blocks:
                            level = self.sample_dict[block[pos]][f]
                            freq[level] = freq.get(level, 0) + 1
                        ideal = len(complete_blocks) / self.levels[f]
                        for level_count in freq.values():
                            cost_pos += abs(level_count - ideal)
            return cost_adj + cost_pos

        current_order = flattened_order(self.blocks)
        current_cost = cost(current_order, self.blocks)

        for it in range(iterations):
            improvement = False
            for block_index, block in enumerate(self.blocks):
                best_perm = block
                best_cost = current_cost
                for perm in set(itertools.permutations(block)):
                    new_blocks = self.blocks.copy()
                    new_blocks[block_index] = list(perm)
                    new_order = flattened_order(new_blocks)
                    new_cost = cost(new_order, new_blocks)
                    if new_cost < best_cost:
                        best_cost = new_cost
                        best_perm = list(perm)
                if list(block) != best_perm:
                    self.blocks[block_index] = best_perm
                    current_cost = best_cost
                    improvement = True
            if not improvement:
                break
        print(f"Intra-block reshuffling completed. Final cost: {current_cost}")

    def print_blocks_pretty(self):
        # Optimize the order within blocks before printing.
        self.intra_block_reshuffle(iterations=10)
        for b_idx, block in enumerate(self.blocks):
            print(f"Block {b_idx}:")
            for sid in block:
                sample = self.sample_dict[sid]
                labeled_sample = self.convert_sample_to_labels(sample)
                sample_name = self.sample_name_dict[sid]
                print(f"  Sample {sid+1} (sample_name: {sample_name}): {labeled_sample}")
            print()

    def convert_sample_to_labels(self, sample):
        labeled = []
        for i, val in enumerate(sample):
            factor = self.factors[i]
            if factor in self.labels:
                labeled.append(self.labels[factor][val])
            else:
                labeled.append(val)
        return tuple(labeled)

    def save_to_csv(self, filename="queue_design.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            header = ["sample_number", "sample_name", "block_index"] + self.factors + ["acquisition_index"]
            writer.writerow(header)
            acquisition_index = 1
            for b_idx, block in enumerate(self.blocks):
                for sid in block:
                    sample = self.sample_dict[sid]
                    labeled_sample = self.convert_sample_to_labels(sample)
                    sample_name = self.sample_name_dict[sid]
                    row = [sid, sample_name, b_idx] + list(labeled_sample) + [acquisition_index]
                    writer.writerow(row)
                    acquisition_index += 1
        print(f"Queue design saved to {filename}")

