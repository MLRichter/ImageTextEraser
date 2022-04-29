from pathlib import Path

from imagetexteraser.backends import SimpleEastBackend, EastMTCNNComposite
from imagetexteraser.modification import bbox
from model_factories import east_model, composit_model


def face_and_text_backend(model_state: Path = "weights/frozen_east_text_detection.pb"):
    net, inf = composit_model(model_state)
    return EastMTCNNComposite(net=net, inference=inf)


def standard_east_backend(model_state: Path = "weights/frozen_east_text_detection.pb"):
    net, inf = east_model(model_state)
    return SimpleEastBackend(net=net, inference=inf)


def debug_east_backend(model_state: Path = "weights/frozen_east_text_detection.pb"):
    net, inf = east_model(model_state)
    return SimpleEastBackend(net=net, inference=inf, modifier=bbox)


if __name__ == '__main__':
    backend = debug_east_backend()
    for _ in backend.process_images(
            src_folder=Path("../test_images"),
            tgt_folder=Path("../results"),
            confidence=0.5
    ):
        continue