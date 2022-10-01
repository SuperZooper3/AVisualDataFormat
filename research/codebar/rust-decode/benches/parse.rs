use codebars::decode::decode;
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("parse 1", |b| b.iter(|| decode(black_box("images/printed.png".to_string()))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);