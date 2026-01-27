use cpal::traits::{DeviceTrait, HostTrait};

fn main() {
    let device = cpal::default_host()
        .default_output_device()
        .expect("no audio output device available");
    println!(
        "Output device: {}",
        device.description().expect("no device description")
    );
}
