import argparse
import struct

def patch_binary(original_file, patch_file, output_file):
  try:
    print(f"[ ] Patching '{original_file}' with '{patch_file}'...")

    # Read original binary file
    with open(original_file, 'rb') as f:
      original_data = f.read()

    # Read patch file (already compiled)
    with open(patch_file, 'rb') as f:
      patch_data = f.read()

    # Append patch to the end of the original data
    modified_data = original_data + patch_data

    # Calculate offsets and modify jump/call instructions as needed
    jump_offset = 0x100  # Example offset
    patch_start_offset = len(original_data)  # Start of the appended patch

    # Example x86 jump instruction (adjust for different architectures)
    jump_instruction = b'\xE9'

    # Calculate relative jump distance considering jump instruction size (typically 5 bytes)
    jump_target = patch_start_offset - jump_offset - len(jump_instruction)

    # Use struct to pack jump target in little-endian format (adjust based on architecture)
    jump_target_bytes = struct.pack('<I', jump_target)  # '<I' for little-endian unsigned int

    modified_data = modified_data[:jump_offset] + jump_instruction + jump_target_bytes + modified_data[jump_offset + len(jump_instruction):]

    # Write modified data to output file
    with open(output_file, 'wb') as f:
      f.write(modified_data)

    print(f"[+] Patching complete. Output saved to '{output_file}'.")

  except FileNotFoundError:
    print("Error: One or more files not found. Please check your file paths and try again.")
  except IOError as e:
    print(f"Error: IO error occurred - {e}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Patch a binary file with a compiled patch.")
  parser.add_argument("original_file", help="Path to the original binary file.")
  parser.add_argument("patch_file", help="Path to the compiled patch file.")
  parser.add_argument("output_file", help="Path to save the patched output file.")

  # Add a flag to show help message
  parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")

  args = parser.parse_args()

  patch_binary(args.original_file, args.patch_file, args.output_file)
